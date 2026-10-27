"""PawPal+ core domain classes (Phase 1 scaffolding)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
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
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks


@dataclass
class Owner:
    """A pet owner and the pets they care for."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every task across all pets as (pet, task) pairs."""
        pass


@dataclass
class Scheduler:
    """Organizes an owner's pet-care tasks into a readable schedule."""

    owner: Owner

    def sort_by_time(
        self, entries: list[tuple[Pet, Task]]
    ) -> list[tuple[Pet, Task]]:
        """Return entries ordered by scheduled date and time."""
        pass

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[tuple[Pet, Task]]:
        """Return the owner's tasks filtered by pet name and/or completion status."""
        pass

    def detect_conflicts(self, entries: list[tuple[Pet, Task]]) -> list[str]:
        """Return warnings for pending tasks that share an identical scheduled time."""
        pass

    def mark_task_complete(self, pet: Pet, task: Task) -> Optional[Task]:
        """Complete a pet's task and return its next occurrence, if any."""
        pass

    def get_daily_schedule(self, day: date) -> list[tuple[Pet, Task]]:
        """Return all tasks for the given day, completed and pending, in time order."""
        pass

    def explain_plan(self, day: date) -> str:
        """Explain the day's ordering, priority labels, and exact-time conflicts."""
        pass
