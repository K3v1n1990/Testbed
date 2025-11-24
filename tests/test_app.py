from argparse import Namespace
from pathlib import Path

from dog_training_app import app
from dog_training_app import models
from dog_training_app import storage


def test_record_session_creates_log(tmp_path: Path) -> None:
    data_file = tmp_path / "logs.json"
    args = Namespace(
        exercise="Sit",
        duration=4,
        treats=2,
        mood="calm",
        notes="Worked on indoors focus",
        data_file=data_file,
    )

    message = app.record_session(args)

    assert "Recorded session" in message
    logs = storage.load_logs(data_file)
    assert len(logs) == 1
    assert logs[0].exercise == "Sit"
    assert logs[0].duration_minutes == 4
    assert logs[0].treats_used == 2
    assert logs[0].mood == "calm"
    assert "indoors focus" in logs[0].notes


def test_progress_summary(tmp_path: Path) -> None:
    data_file = tmp_path / "logs.json"
    storage.clear_data(data_file)
    storage.append_log(models.SessionLog("Sit", 3, 1, "calm", ""), data_file)
    storage.append_log(models.SessionLog("Stay", 5, 0, "calm", ""), data_file)
    storage.append_log(models.SessionLog("Sit", 2, 2, "playful", ""), data_file)

    summary = app.render_progress(data_file)

    assert "Total sessions: 3" in summary
    assert "Sit: 2 session(s)" in summary
    assert "Stay: 1 session(s)" in summary


def test_render_exercises_includes_steps() -> None:
    output = app.render_exercises(show_details=True)

    assert "Sit: Dog sits on command" in output
    assert "Hold a treat close" in output


def test_summarize_logs_counts_totals() -> None:
    logs = [
        models.SessionLog("Sit", 3, 1, "calm", ""),
        models.SessionLog("Sit", 2, 0, "calm", ""),
        models.SessionLog("Stay", 5, 2, "tired", ""),
    ]

    summary = models.summarize_logs(logs)

    assert summary["sessions"] == 3
    assert summary["total_minutes"] == 10
    assert summary["total_treats"] == 3
    assert summary["per_exercise"] == {"Sit": 2, "Stay": 1}
