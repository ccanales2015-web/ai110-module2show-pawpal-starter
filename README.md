# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output of `python main.py`, which builds one owner, two pets, and five tasks for October 27, 2026, then demonstrates chronological sorting and filtering by pet and completion status:

```text
=== Initial schedule ===
Plan for 2026-10-27
Tasks are listed in order of scheduled time. Priority labels are informational and do not change the order.

  08:00  Morning walk (Rex) - high priority, pending
  08:00  Quick check (Rex) - high priority, pending
  08:00  Breakfast (Mochi) - medium priority, pending
  08:10  Meds (Rex) - high priority, pending
  19:00  Brush fur (Mochi) - low priority, pending

Conflicts (overlapping pending tasks for the same pet):
  - Conflict at 2026-10-27 08:00: Morning walk (Rex, 08:00-08:30), Quick check (Rex, 08:00-08:05)
  - Conflict at 2026-10-27 08:10: Morning walk (Rex, 08:00-08:30), Meds (Rex, 08:10-08:20)

=== After completing Rex's morning walk ===
Plan for 2026-10-27
Tasks are listed in order of scheduled time. Priority labels are informational and do not change the order.

  08:00  Morning walk (Rex) - high priority, completed
  08:00  Quick check (Rex) - high priority, pending
  08:00  Breakfast (Mochi) - medium priority, pending
  08:10  Meds (Rex) - high priority, pending
  19:00  Brush fur (Mochi) - low priority, pending

No overlapping tasks detected for the same pet.

=== Next occurrence ===
Morning walk (Rex) is next scheduled for 2026-10-28 08:00 (daily, high priority)

=== Sorting Mochi's tasks by time ===
In the order they were added:
  2026-10-27 19:00  Brush fur (Mochi)
  2026-10-27 08:00  Breakfast (Mochi)
After sort_by_time():
  2026-10-27 08:00  Breakfast (Mochi)
  2026-10-27 19:00  Brush fur (Mochi)

=== Filtering tasks ===
Rex's pending tasks (pet_name='Rex', completed=False):
  2026-10-27 08:00  Quick check (Rex)
  2026-10-27 08:10  Meds (Rex)
  2026-10-28 08:00  Morning walk (Rex)
All completed tasks (completed=True):
  2026-10-27 08:00  Morning walk (Rex)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest
```

Add `-v` to list each test by name.

The tests in `tests/test_pawpal.py` cover:

- **Task basics:** marking a task complete and adding tasks to a pet.
- **Chronological sorting:** `sort_by_time()` returns out-of-order `(pet, task)` pairs earliest first, including a task on a later day with an earlier time of day, keeps each task paired with its pet, and leaves the input list unchanged.
- **Daily recurrence:** completing a `daily` task adds a pending copy one day later with the same description, duration, priority, and frequency.
- **Conflict detection:** overlapping pending tasks for the same pet produce a warning, including tasks with identical start times.
- **Edge cases:** back-to-back tasks, overlapping tasks for different pets, and completed tasks do not conflict; one-off tasks get no next occurrence; completing a task for the wrong pet raises `ValueError` and changes nothing; completing an already-completed `weekly` task a second time is a no-op.

Sample test output (machine-specific header lines omitted):

```
collected 12 items

tests\test_pawpal.py ............                                        [100%]

============================= 12 passed in 0.05s ==============================
```

**Confidence level: ★★★★☆ (4/5)**

All 12 tests pass, and they exercise the core scheduling behaviors and their main edge cases. Passing tests do not prove the system is bug-free, though. `filter_tasks()`, `get_daily_schedule()`, `explain_plan()`, `Task` input validation, and the Streamlit UI have no direct automated tests yet.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders `(pet, task)` pairs by `scheduled_at`, earliest first. Tasks with the same start time keep their original order. Priority is shown as a label but does not change the order. |
| Filtering | `Scheduler.filter_tasks()` | Filters the owner's tasks by `pet_name` (exact, case-sensitive match) and/or `completed` (`True` or `False`). Leaving either argument as `None` skips that filter. Results keep the order pets and tasks were added and are not sorted. |
| Conflict handling | `Scheduler.detect_conflicts()` | Each task occupies `[scheduled_at, scheduled_at + duration_minutes)` (default 20 minutes), so back-to-back tasks do not conflict. Only pending tasks belonging to the same pet are compared; completed tasks and tasks of different pets never conflict. Each overlapping pair produces one warning. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a `daily` or `weekly` task keeps it as completed and adds a new pending copy 1 or 7 days later to the same pet, with the same description, duration, priority, and frequency. One-off (`none`) tasks get no copy. Completing an already-completed task changes nothing, and a task that does not belong to the given pet raises `ValueError`. |

## 📸 Demo Walkthrough

Follow these steps in the Streamlit app:

1. **Add a pet.** Under **Owner and Pet Management**, enter a **Pet name**, choose a **Species**, and click **Add pet**. The pet should appear in the **Current pets** table.
2. **Create tasks with durations.** Under **Tasks**, choose the **Pet**, enter a **Task title**, **Date**, and **Time**, choose a **Frequency** and **Priority**, set **Duration (minutes)** (1–240; default 20), and click **Add task**. To see a conflict, add another task for the same pet that starts before the first task ends. Both tasks should appear in **Current tasks**.
3. **Generate a schedule and review conflicts.** Under **Build Schedule**, choose the **Schedule date** and click **Generate schedule**. The plan lists that day's tasks in time order and reports any overlapping pending tasks for the same pet, or states that no such overlaps were detected.
4. **Mark a task complete.** Choose a task from the **Pending task** dropdown and click **Mark complete**. A confirmation appears and the task's status changes to `completed` in the **Current tasks** table. Completing a daily or weekly task also adds its next occurrence as a new pending task.
5. **Regenerate the schedule.** Click **Generate schedule** again to view the updated plan. Completed tasks are no longer checked for conflicts.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
