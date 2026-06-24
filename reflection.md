# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

1. **Add owner and pet information** — The user enters basic profile details such as the owner's name, the pet's name, breed, and any relevant preferences (e.g., preferred walk times). This establishes the context the scheduler uses when building a plan.

2. **Add and edit care tasks** — The user creates individual tasks (walks, feeding, medication, grooming, enrichment, etc.) and assigns each a duration and a priority level. Tasks can be updated or removed as the pet's needs change, giving the owner full control over what gets scheduled.

3. **Generate and view the daily schedule** — The user requests a daily plan, and the app produces an ordered list of tasks fitted to the owner's available time window. The plan shows the scheduled time, duration, and priority of each task, and explains why tasks were chosen or skipped (e.g., lower-priority tasks dropped when time runs out).

**a. Initial design**

The initial design uses four classes defined in `pawpal_system.py`:

- **Task** (dataclass) — The smallest unit of work. It holds a `title`, `duration_minutes`, `priority` ("low" / "medium" / "high"), a `recurring` flag, and optional `notes`. Its only behavioral method is `is_high_priority()`. Task is a pure data object with no knowledge of pets or owners.

- **Pet** (dataclass) — Represents the animal being cared for. It stores profile details (`name`, `species`, `breed`, `age_years`) and owns a list of `Task` objects. It provides `add_task()` and `get_tasks()` to manage that list. Pet knows nothing about scheduling — it is purely a data container.

- **Owner** (dataclass) — Represents the person responsible for the pet. It stores `name`, `available_minutes` (total care time available in a day), and `preferred_start_time`. It owns a list of `Pet` objects and provides `add_pet()` / `get_pets()`. Owner preferences (available time, start time) are the primary scheduling constraints.

- **Scheduler** — The only class with real logic. It takes an `Owner` and a `Pet` at construction time and exposes a `generate_plan()` method that returns `{"scheduled": [...], "skipped": [...]}`. Internally it delegates to `sort_tasks()` (sort by priority then duration) and `filter_tasks()` (greedy selection within `available_minutes`). An `explain_plan()` method produces a human-readable summary of the reasoning.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
