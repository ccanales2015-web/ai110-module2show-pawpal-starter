from datetime import datetime

from pawpal_system import Task


def test_mark_complete_changes_task_status():
    task = Task("Morning walk", datetime(2026, 10, 27, 8, 0))

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True
