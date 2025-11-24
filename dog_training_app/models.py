from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Iterable, List


@dataclass
class Exercise:
    """Represents a single training exercise."""

    name: str
    goal: str
    steps: List[str]
    recommended_duration: int


@dataclass
class SessionLog:
    """Represents a single recorded training session."""

    exercise: str
    duration_minutes: int
    treats_used: int
    mood: str
    notes: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, str | int]:
        return {
            "exercise": self.exercise,
            "duration_minutes": self.duration_minutes,
            "treats_used": self.treats_used,
            "mood": self.mood,
            "notes": self.notes,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str | int]) -> "SessionLog":
        return cls(
            exercise=str(data.get("exercise", "")),
            duration_minutes=int(data.get("duration_minutes", 0)),
            treats_used=int(data.get("treats_used", 0)),
            mood=str(data.get("mood", "")),
            notes=str(data.get("notes", "")),
            timestamp=str(data.get("timestamp", datetime.now(timezone.utc).isoformat())),
        )


def summarize_logs(logs: Iterable[SessionLog]) -> Dict[str, int | Dict[str, int]]:
    """Aggregate high-level statistics from a collection of session logs."""

    total_minutes = 0
    total_treats = 0
    per_exercise: Dict[str, int] = {}

    for log in logs:
        total_minutes += log.duration_minutes
        total_treats += log.treats_used
        per_exercise[log.exercise] = per_exercise.get(log.exercise, 0) + 1

    return {
        "sessions": sum(per_exercise.values()),
        "total_minutes": total_minutes,
        "total_treats": total_treats,
        "per_exercise": per_exercise,
    }
