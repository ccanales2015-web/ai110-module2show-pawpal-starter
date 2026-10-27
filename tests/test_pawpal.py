from datetime import datetime

from pawpal_system import Pet, Task


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
