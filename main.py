"""Command-line demonstration of the PawPal+ scheduling system."""

from datetime import date, datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    """Build a sample owner, pets, and tasks, then print the daily plan."""
    demo_day = date(2026, 10, 27)

    owner = Owner("Jordan")
    rex = Pet("Rex", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(rex)
    owner.add_pet(mochi)

    walk = Task(
        "Morning walk",
        datetime(2026, 10, 27, 8, 0),
        frequency="daily",
        priority="high",
    )
    breakfast = Task("Breakfast", datetime(2026, 10, 27, 8, 0), priority="medium")
    brushing = Task(
        "Brush fur",
        datetime(2026, 10, 27, 19, 0),
        frequency="weekly",
        priority="low",
    )
    rex.add_task(walk)
    mochi.add_task(brushing)
    mochi.add_task(breakfast)

    scheduler = Scheduler(owner)

    print("=== Initial schedule ===")
    print(scheduler.explain_plan(demo_day))
    print()

    next_walk = scheduler.mark_task_complete(rex, walk)

    print("=== After completing Rex's morning walk ===")
    print(scheduler.explain_plan(demo_day))
    print()

    print("=== Next occurrence ===")
    if next_walk is not None:
        print(
            f"{next_walk.description} ({rex.name}) is next scheduled for "
            f"{next_walk.scheduled_at:%Y-%m-%d %H:%M} "
            f"({next_walk.frequency}, {next_walk.priority} priority)"
        )
    else:
        print("No next occurrence was created.")


if __name__ == "__main__":
    main()
