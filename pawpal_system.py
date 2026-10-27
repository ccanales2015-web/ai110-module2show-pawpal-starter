"""PawPal+ core domain classes (Phase 1 scaffolding)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(eq=False)
class Task:
    """A single pet-care task scheduled at a specific date and time."""

    description: str
    scheduled_at: datetime
    frequency: str = "none"
    priority: str = "medium"
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate frequency and priority values."""
        pass

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def next_occurrence(self) -> Optional[Task]:
        """Return the next occurrence of a recurring task, or None."""
        pass


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        pass
