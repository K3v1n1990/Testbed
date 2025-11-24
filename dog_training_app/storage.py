from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .models import SessionLog

DEFAULT_DATA_PATH = Path.home() / ".dog_training_app" / "training_data.json"


def ensure_data_file(path: Path = DEFAULT_DATA_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps({"logs": []}, indent=2))
    return path


def load_logs(path: Path = DEFAULT_DATA_PATH) -> List[SessionLog]:
    ensure_data_file(path)
    with path.open() as fp:
        raw = json.load(fp)
    logs = raw.get("logs", []) if isinstance(raw, dict) else []
    return [SessionLog.from_dict(entry) for entry in logs]


def save_logs(logs: List[SessionLog], path: Path = DEFAULT_DATA_PATH) -> None:
    ensure_data_file(path)
    serializable = {"logs": [log.to_dict() for log in logs]}
    path.write_text(json.dumps(serializable, indent=2))


def append_log(log: SessionLog, path: Path = DEFAULT_DATA_PATH) -> None:
    logs = load_logs(path)
    logs.append(log)
    save_logs(logs, path)


def clear_data(path: Path = DEFAULT_DATA_PATH) -> None:
    """Reset the data file for a fresh start."""

    ensure_data_file(path)
    path.write_text(json.dumps({"logs": []}, indent=2))
