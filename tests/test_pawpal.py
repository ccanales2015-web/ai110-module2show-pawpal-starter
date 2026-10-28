from datetime import datetime

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status():
    task = Task("Morning walk", datetime(2026, 10, 27, 8, 0))

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Rex", "dog")

    assert len(pet.get_tasks()) == 0

    task = Task("Morning walk", datetime(2026, 10, 27, 8, 0))
    pet.add_task(task)

    assert len(pet.get_tasks()) == 1


def conflicts_for(*pets):
    owner = Owner("Jordan")
    for pet in pets:
        owner.add_pet(pet)
    return Scheduler(owner).detect_conflicts(owner.get_all_tasks())


def test_same_pet_overlapping_tasks_conflict():
    rex = Pet("Rex", "dog")
    rex.add_task(Task("Walk", datetime(2026, 10, 27, 8, 0), duration_minutes=30))
    rex.add_task(Task("Brush", datetime(2026, 10, 27, 8, 15), duration_minutes=10))

    conflicts = conflicts_for(rex)

    assert conflicts == [
        "Conflict at 2026-10-27 08:15: "
        "Walk (Rex, 08:00-08:30), Brush (Rex, 08:15-08:25)"
    ]


def test_same_pet_back_to_back_tasks_do_not_conflict():
    rex = Pet("Rex", "dog")
    rex.add_task(Task("Walk", datetime(2026, 10, 27, 8, 0), duration_minutes=30))
    rex.add_task(Task("Breakfast", datetime(2026, 10, 27, 8, 30), duration_minutes=15))

    assert conflicts_for(rex) == []


def test_overlapping_tasks_for_different_pets_do_not_conflict():
    rex = Pet("Rex", "dog")
    mochi = Pet("Mochi", "cat")
    rex.add_task(Task("Walk", datetime(2026, 10, 27, 8, 0), duration_minutes=30))
    mochi.add_task(Task("Breakfast", datetime(2026, 10, 27, 8, 10), duration_minutes=20))

    assert conflicts_for(rex, mochi) == []


def test_completed_task_overlapping_pending_task_does_not_conflict():
    rex = Pet("Rex", "dog")
    walk = Task("Walk", datetime(2026, 10, 27, 8, 0), duration_minutes=30)
    walk.mark_complete()
    rex.add_task(walk)
    rex.add_task(Task("Brush", datetime(2026, 10, 27, 8, 15), duration_minutes=10))

    assert conflicts_for(rex) == []


def test_same_pet_identical_start_times_conflict():
    rex = Pet("Rex", "dog")
    rex.add_task(Task("Walk", datetime(2026, 10, 27, 8, 0), duration_minutes=30))
    rex.add_task(Task("Meds", datetime(2026, 10, 27, 8, 0), duration_minutes=5))

    conflicts = conflicts_for(rex)

    assert len(conflicts) == 1
    assert conflicts[0].startswith("Conflict at 2026-10-27 08:00: ")
    assert "Walk (Rex, 08:00-08:30)" in conflicts[0]
    assert "Meds (Rex, 08:00-08:05)" in conflicts[0]


def test_completing_daily_task_adds_next_occurrence():
    owner = Owner("Jordan")
    rex = Pet("Rex", "dog")
    owner.add_pet(rex)
    walk = Task(
        "Walk",
        datetime(2026, 10, 27, 8, 0),
        frequency="daily",
        priority="high",
        duration_minutes=30,
    )
    rex.add_task(walk)

    next_walk = Scheduler(owner).mark_task_complete(rex, walk)

    assert walk.completed is True
    assert rex.get_tasks() == [walk, next_walk]
    assert next_walk.completed is False
    assert next_walk.description == "Walk"
    assert next_walk.scheduled_at == datetime(2026, 10, 28, 8, 0)
    assert next_walk.duration_minutes == 30
    assert next_walk.priority == "high"
    assert next_walk.frequency == "daily"


def test_completing_one_off_task_does_not_add_occurrence():
    owner = Owner("Jordan")
    rex = Pet("Rex", "dog")
    owner.add_pet(rex)
    vet = Task("Vet visit", datetime(2026, 10, 27, 14, 0))
    rex.add_task(vet)

    next_task = Scheduler(owner).mark_task_complete(rex, vet)

    assert next_task is None
    assert vet.completed is True
    assert rex.get_tasks() == [vet]


def test_completing_task_for_wrong_pet_raises_and_changes_nothing():
    owner = Owner("Jordan")
    rex = Pet("Rex", "dog")
    mochi = Pet("Mochi", "cat")
    owner.add_pet(rex)
    owner.add_pet(mochi)
    walk = Task("Walk", datetime(2026, 10, 27, 8, 0), frequency="daily")
    breakfast = Task("Breakfast", datetime(2026, 10, 27, 8, 0))
    rex.add_task(walk)
    mochi.add_task(breakfast)

    with pytest.raises(ValueError):
        Scheduler(owner).mark_task_complete(mochi, walk)

    assert walk.completed is False
    assert rex.get_tasks() == [walk]
    assert mochi.get_tasks() == [breakfast]


def test_completing_already_completed_recurring_task_is_a_no_op():
    owner = Owner("Jordan")
    rex = Pet("Rex", "dog")
    owner.add_pet(rex)
    brushing = Task(
        "Brush fur",
        datetime(2026, 10, 27, 19, 0),
        frequency="weekly",
    )
    rex.add_task(brushing)
    scheduler = Scheduler(owner)

    next_brushing = scheduler.mark_task_complete(rex, brushing)

    assert brushing.completed is True
    assert rex.get_tasks() == [brushing, next_brushing]
    assert next_brushing.scheduled_at == datetime(2026, 11, 3, 19, 0)

    assert scheduler.mark_task_complete(rex, brushing) is None
    assert rex.get_tasks() == [brushing, next_brushing]
    assert next_brushing.completed is False
