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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
