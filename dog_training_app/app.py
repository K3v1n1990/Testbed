from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent
from typing import List

from .models import SessionLog, summarize_logs
from .presets import default_exercises
from .storage import DEFAULT_DATA_PATH, append_log, load_logs

MOOD_CHOICES = ["calm", "distracted", "playful", "tired"]


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dog-trainer",
        description="Coach yourself through foundational dog training exercises and track sessions.",
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Where to store training logs (defaults to ~/.dog_training_app/training_data.json).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    exercises_parser = subparsers.add_parser("exercises", help="List recommended exercises.")
    exercises_parser.add_argument("--details", action="store_true", help="Show full steps for each exercise.")

    start_parser = subparsers.add_parser("start", help="Record a training session.")
    start_parser.add_argument("exercise", help="Exercise name (e.g. Sit, Stay, Down, Come).")
    start_parser.add_argument("--duration", type=int, default=None, help="Session length in minutes.")
    start_parser.add_argument("--treats", type=int, default=0, help="Treats used during training.")
    start_parser.add_argument("--mood", choices=MOOD_CHOICES, default="calm", help="Dog's energy level.")
    start_parser.add_argument("--notes", default="", help="Observations or reminders for next time.")

    subparsers.add_parser("progress", help="View progress across exercises.")
    subparsers.add_parser("tips", help="Show general training best practices.")

    return parser


def render_exercises(show_details: bool = False) -> str:
    lines: List[str] = []
    for exercise in default_exercises():
        lines.append(f"- {exercise.name}: {exercise.goal} (recommended {exercise.recommended_duration} minutes)")
        if show_details:
            for step in exercise.steps:
                lines.append(f"    • {step}")
    return "\n".join(lines)


def record_session(args: argparse.Namespace) -> str:
    exercises = {ex.name.lower(): ex for ex in default_exercises()}
    chosen = exercises.get(args.exercise.lower())
    if not chosen:
        raise SystemExit(f"Unknown exercise '{args.exercise}'. Try one of: {', '.join(exercises.keys())}.")

    duration = args.duration if args.duration is not None else chosen.recommended_duration
    log = SessionLog(
        exercise=chosen.name,
        duration_minutes=max(duration, 1),
        treats_used=max(args.treats, 0),
        mood=args.mood,
        notes=args.notes,
    )
    append_log(log, path=args.data_file)
    return (
        "Recorded session:\n"
        f"- Exercise: {log.exercise}\n"
        f"- Duration: {log.duration_minutes} minutes\n"
        f"- Treats: {log.treats_used}\n"
        f"- Mood: {log.mood}\n"
        f"- Notes: {log.notes or 'None'}"
    )


def render_progress(path: Path) -> str:
    logs = load_logs(path)
    if not logs:
        return "No training logs yet. Start with `dog-trainer start Sit`!"

    summary = summarize_logs(logs)
    per_ex = "\n".join(
        f"- {name}: {count} session(s)" for name, count in sorted(summary["per_exercise"].items())
    )
    return dedent(
        f"""
        Progress overview
        ----------------
        Total sessions: {summary['sessions']}
        Total time: {summary['total_minutes']} minutes
        Treats used: {summary['total_treats']}

        Per exercise:
        {per_ex}
        """
    ).strip()


def render_tips() -> str:
    tips = [
        "Keep sessions short and end on a positive note.",
        "Reward calm behavior, not just excitement.",
        "Practice in distraction-free environments before adding challenges.",
        "Be consistent with cues and hand signals across family members.",
        "Log how your dog felt to spot patterns over time.",
    ]
    return "\n".join(f"- {tip}" for tip in tips)


def main(argv: list[str] | None = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command == "exercises":
        print(render_exercises(args.details))
    elif args.command == "start":
        print(record_session(args))
    elif args.command == "progress":
        print(render_progress(args.data_file))
    elif args.command == "tips":
        print(render_tips())
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()
