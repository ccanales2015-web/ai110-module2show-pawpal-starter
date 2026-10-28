# PawPal+ Project Reflection

## 1. System Design

**Core User Actions**

1. **Add and manage pets:** The owner can register pets and maintain their basic information.
2. **Schedule pet-care tasks:** The owner can create care tasks, such as feeding, walking, and medication, and assign scheduled times to them.
3. **View an organized daily care plan:** The owner can view scheduled tasks in chronological order and receive explanations of any scheduling conflicts.

**a. Initial design**

I designed PawPal+ around four classes: `Owner`, `Pet`, `Task`, and `Scheduler`.

The `Owner` class stores the owner's name and pets and provides access to their associated tasks. The `Pet` class stores basic information about each pet and manages that pet's care tasks.

The `Task` class represents an individual pet-care activity, including its description, scheduled date and time, recurrence frequency, priority, and completion status. It also handles marking tasks complete and calculating the next occurrence of recurring tasks.

The `Scheduler` class organizes tasks chronologically, filters them by pet or completion status, detects scheduling conflicts, and coordinates recurring-task completion. It also produces daily schedules and explains how those schedules are organized.

I separated these responsibilities to keep the design modular and avoid duplicating task information. Each pet owns its tasks, while the scheduler accesses them through the owner. The initial design prioritizes straightforward scheduling and conflict detection rather than automatic schedule optimization.

**b. Design changes**

Yes. During the initial Python scaffolding, I decided to implement the `Owner` and `Scheduler` classes as dataclasses, alongside `Pet` and `Task`.

This allowed Python to generate their constructors automatically, reducing boilerplate code while preserving the responsibilities and relationships established in the original design.

I subsequently updated the UML diagram to identify `Owner` and `Scheduler` as dataclasses, keeping the diagram consistent with the Python implementation. The overall four-class architecture remained unchanged.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

I prioritized keeping the scheduling logic simple and understandable while allowing the owner to remain in control of scheduling decisions. The scheduler sorts tasks chronologically, uses task duration to detect overlapping pending tasks for the same pet, and reports conflicts as warnings rather than automatically changing the schedule. Task priority is displayed as information but does not override chronological ordering. This design makes the scheduling behavior predictable and easier to understand, although it means the owner must resolve conflicts manually and high-priority tasks are not automatically scheduled first.

**b. Tradeoffs**

One tradeoff in my scheduler is that it reports scheduling conflicts as warnings instead of automatically rescheduling tasks. When two pending tasks for the same pet overlap, the system identifies the conflict and displays the tasks' time ranges. It does not move, remove, or reprioritize either task. This keeps the owner in control of the schedule and avoids making assumptions about which task can be moved. The tradeoff is that the owner must resolve conflicts manually. I consider this reasonable because different pet-care tasks may have constraints that the program does not understand.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI as a collaborator throughout the project rather than accepting large code changes without review. We worked in small steps: proposing changes, reviewing the diffs, approving specific edits, and running tests to verify the results. The most helpful use of AI was developing targeted tests for scheduling behavior and interpreting the results. For example, we added tests for overlapping tasks, back-to-back tasks, recurring tasks, and attempts to complete a task assigned to the wrong pet. This incremental approach helped me verify individual behaviors and catch potential problems before moving on to the next step.

**b. Judgment and verification**

One moment when I did not accept an AI suggestion without evaluating it was when we considered simplifying the scheduler's conflict-detection algorithm. The alternative was easier to follow in some respects, but it would compare every pair of tasks and could change the order in which conflicts were reported. I evaluated the suggestion by comparing the readability and efficiency of both approaches and considering its effects on the existing tests, README, and UML diagram. I decided to keep the existing implementation because it was already tested, efficient for the intended use, and consistent with the documented behavior. This reinforced the importance of evaluating AI suggestions rather than assuming that a proposed simplification is necessarily an improvement.

---

## 4. Testing and Verification

**a. What you tested**

I tested the scheduler's core behaviors using automated pytest tests. These included marking tasks as complete, adding tasks to a pet, detecting overlapping tasks for the same pet, allowing back-to-back tasks, ignoring overlaps between different pets, and excluding completed tasks from conflict detection. I also tested tasks with identical start times, the creation of the next occurrence for daily tasks, the absence of a new occurrence for one-off tasks, rejection of a task belonging to the wrong pet, and repeated completion of an already-completed recurring task. These tests were important because they checked both expected behavior and edge cases that could otherwise lead to incorrect schedules or unintended changes. All 11 tests passed.

**b. Confidence**

I am very confident that the current implementation satisfies the requirements we have tested. All 11 automated tests pass, including tests for overlapping task durations, recurring tasks, and invalid completion attempts. The tests cover both normal operations and important edge cases. However, passing tests cannot prove that every possible situation has been handled correctly. With more time, I would test the Streamlit interface more extensively, including how it behaves when users enter invalid data, create many tasks, or schedule tasks that overlap across midnight.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the scheduler's conflict-detection logic. Instead of checking only whether two tasks have exactly the same start time, the system considers each task's duration and detects when two pending tasks for the same pet overlap. It also correctly allows back-to-back tasks and ignores completed tasks and tasks belonging to different pets. I am particularly satisfied that these behaviors are covered by automated tests. This makes the scheduler more useful for realistic pet-care scheduling than a simple list of tasks ordered by start time.

**b. What you would improve**

If I had another iteration, I would add data persistence so that pets and their scheduled tasks are saved between application sessions. Currently, the application stores its data in memory, so restarting it can cause the data to be lost. Saving the information to a file or database would make PawPal+ more practical for everyday use. I would also ensure that saved data is loaded when the application starts and that changes are saved reliably as users add pets, schedule tasks, and mark tasks as complete.

**c. Key takeaway**

One important takeaway from this project is that good software development requires more than writing code that works in simple cases. Algorithms need to reflect real-world requirements and account for edge cases, such as tasks that overlap in duration rather than merely sharing a start time. I also learned that AI-generated suggestions need to be evaluated and verified through reasoning and testing rather than accepted automatically. Finally, the project showed me how the backend logic, user interface, automated tests, and documentation depend on one another. A change to one component can affect the others, so testing and maintaining consistency across the system are important parts of software development.
