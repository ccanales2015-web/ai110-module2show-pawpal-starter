"""PawPal+ core domain classes (Phase 1 scaffolding)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional


@dataclass(eq=False)
class Task:
    """A single pet-care task scheduled at a specific date and time."""

    description: str
    scheduled_at: datetime
    frequency: str = "none"
    priority: str = "medium"
    completed: bool = False
    duration_minutes: int = 20

    def __post_init__(self) -> None:
        """Validate frequency, priority, and duration values."""
        valid_frequencies = ("none", "daily", "weekly")
        valid_priorities = ("low", "medium", "high")
        if self.frequency not in valid_frequencies:
            raise ValueError(
                f"Invalid frequency {self.frequency!r}; "
                f"expected one of {valid_frequencies}"
            )
        if self.priority not in valid_priorities:
            raise ValueError(
                f"Invalid priority {self.priority!r}; "
                f"expected one of {valid_priorities}"
            )
        if (
            isinstance(self.duration_minutes, bool)
            or not isinstance(self.duration_minutes, int)
            or self.duration_minutes <= 0
        ):
            raise ValueError(
                f"Invalid duration_minutes {self.duration_minutes!r}; "
                f"expected a positive integer"
            )

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional[Task]:
        """Return the next occurrence of a recurring task, or None."""
        if self.frequency == "daily":
            interval = timedelta(days=1)
        elif self.frequency == "weekly":
            interval = timedelta(days=7)
        else:
            return None
        return Task(
            description=self.description,
            scheduled_at=self.scheduled_at + interval,
            frequency=self.frequency,
            priority=self.priority,
            completed=False,
            duration_minutes=self.duration_minutes,
        )


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
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every task across all pets as (pet, task) pairs."""
        return [(pet, task) for pet in self.pets for task in pet.get_tasks()]


@dataclass
class Scheduler:
    """Organizes an owner's pet-care tasks into a readable schedule."""

    owner: Owner

    def sort_by_time(
        self, entries: list[tuple[Pet, Task]]
    ) -> list[tuple[Pet, Task]]:
        """Return entries ordered by scheduled date and time."""
        return sorted(entries, key=lambda entry: entry[1].scheduled_at)

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[tuple[Pet, Task]]:
        """Return the owner's tasks filtered by pet name and/or completion status."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if (pet_name is None or pet.name == pet_name)
            and (completed is None or task.completed == completed)
        ]

    def detect_conflicts(self, entries: list[tuple[Pet, Task]]) -> list[str]:
        """Return warnings for overlapping pending tasks that belong to the same pet.

        Each task occupies [scheduled_at, scheduled_at + duration_minutes), so
        back-to-back tasks do not conflict.
        """
        by_pet: dict[int, list[tuple[Pet, Task]]] = {}
        for pet, task in entries:
            if not task.completed:
                by_pet.setdefault(id(pet), []).append((pet, task))

        def describe(pet: Pet, task: Task, end: datetime) -> str:
            return (
                f"{task.description} ({pet.name}, "
                f"{task.scheduled_at:%H:%M}-{end:%H:%M})"
            )

        found: list[tuple[datetime, str, str]] = []
        for group in by_pet.values():
            group = self.sort_by_time(group)
            for i, (pet, first) in enumerate(group):
                first_end = first.scheduled_at + timedelta(minutes=first.duration_minutes)
                for _, second in group[i + 1:]:
                    if second.scheduled_at >= first_end:
                        break
                    second_end = second.scheduled_at + timedelta(
                        minutes=second.duration_minutes
                    )
                    tasks = (
                        f"{describe(pet, first, first_end)}, "
                        f"{describe(pet, second, second_end)}"
                    )
                    found.append((second.scheduled_at, pet.name, tasks))
        found.sort(key=lambda item: (item[0], item[1]))
        return [f"Conflict at {when:%Y-%m-%d %H:%M}: {tasks}" for when, _, tasks in found]

    def mark_task_complete(self, pet: Pet, task: Task) -> Optional[Task]:
        """Complete a pet's task and return its next occurrence, if any."""
        if not any(existing is task for existing in pet.get_tasks()):
            raise ValueError(
                f"Task {task.description!r} does not belong to pet {pet.name!r}"
            )
        if task.completed:
            return None
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            pet.add_task(next_task)
        return next_task

    def get_daily_schedule(self, day: date) -> list[tuple[Pet, Task]]:
        """Return all tasks for the given day, completed and pending, in time order."""
        return self.sort_by_time(
            [
                (pet, task)
                for pet, task in self.owner.get_all_tasks()
                if task.scheduled_at.date() == day
            ]
        )

    def explain_plan(self, day: date) -> str:
        """Explain the day's ordering, priority labels, and same-pet overlaps."""
        entries = self.get_daily_schedule(day)
        if not entries:
            return f"Plan for {day:%Y-%m-%d}\nNo tasks are scheduled for this day."
        lines = [
            f"Plan for {day:%Y-%m-%d}",
            "Tasks are listed in order of scheduled time. "
            "Priority labels are informational and do not change the order.",
            "",
        ]
        for pet, task in entries:
            status = "completed" if task.completed else "pending"
            lines.append(
                f"  {task.scheduled_at:%H:%M}  {task.description} ({pet.name})"
                f" - {task.priority} priority, {status}"
            )
        conflicts = self.detect_conflicts(entries)
        lines.append("")
        if conflicts:
            lines.append("Conflicts (overlapping pending tasks for the same pet):")
            lines.extend(f"  - {warning}" for warning in conflicts)
        else:
            lines.append("No overlapping tasks detected for the same pet.")
        return "\n".join(lines)
