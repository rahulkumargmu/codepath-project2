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

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from `python3 main.py`:

```
════════════════════════════════════════════════════
  🐾  PawPal+ — Today's Schedule
════════════════════════════════════════════════════

────────────────────────────────────────────────────
Daily plan for Biscuit (dog)
Owner: Jordan  |  Available: 90 min  |  Start: 08:00

Scheduled tasks:
  08:00–08:05  Medication (5 min)  [priority: high] [recurring]
             Note: 1 tablet with food
  08:05–08:15  Feeding (10 min)  [priority: high] [recurring]
  08:15–08:45  Morning walk (30 min)  [priority: high] [recurring]
  08:45–09:05  Enrichment puzzle (20 min)  [priority: medium]

Total time used: 65 / 90 min

Skipped tasks (insufficient time remaining):
  - Grooming (40 min, priority: low)
────────────────────────────────────────────────────

────────────────────────────────────────────────────
Daily plan for Mochi (cat)
Owner: Jordan  |  Available: 45 min  |  Start: 09:30

Scheduled tasks:
  09:30–09:40  Feeding (10 min)  [priority: high] [recurring]
  09:40–09:50  Litter box clean (10 min)  [priority: high] [recurring]
  09:50–10:10  Playtime (20 min)  [priority: medium]
             Note: Feather wand

Total time used: 40 / 45 min

Skipped tasks (insufficient time remaining):
  - Brushing (15 min, priority: low)
────────────────────────────────────────────────────
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-9.1.1
collected 13 items

tests/test_pawpal.py::TestTask::test_mark_complete_changes_status PASSED  [  7%]
tests/test_pawpal.py::TestTask::test_mark_complete_is_idempotent PASSED   [ 15%]
tests/test_pawpal.py::TestTask::test_is_high_priority_true PASSED         [ 23%]
tests/test_pawpal.py::TestTask::test_is_high_priority_false_for_medium PASSED [ 30%]
tests/test_pawpal.py::TestPet::test_add_task_increases_count PASSED       [ 38%]
tests/test_pawpal.py::TestPet::test_add_multiple_tasks PASSED             [ 46%]
tests/test_pawpal.py::TestPet::test_get_tasks_returns_copy PASSED         [ 53%]
tests/test_pawpal.py::TestOwner::test_add_pet_increases_count PASSED      [ 61%]
tests/test_pawpal.py::TestScheduler::test_high_priority_tasks_scheduled_first PASSED [ 69%]
tests/test_pawpal.py::TestScheduler::test_tasks_fit_within_available_time PASSED [ 76%]
tests/test_pawpal.py::TestScheduler::test_low_priority_task_skipped_when_no_time PASSED [ 84%]
tests/test_pawpal.py::TestScheduler::test_all_tasks_scheduled_when_time_is_ample PASSED [ 92%]
tests/test_pawpal.py::TestScheduler::test_explain_plan_contains_pet_name PASSED [100%]

============================== 13 passed in 0.03s ==============================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
