"""
tests/test_pawpal.py — Unit tests for PawPal+ core logic.

Run with:  python3 -m pytest  (or simply: pytest)
"""

import pytest
from pawpal_system import Owner, Pet, Scheduler, Task


# ---------------------------------------------------------------------------
# Task tests
# ---------------------------------------------------------------------------

class TestTask:
    def test_mark_complete_changes_status(self):
        """mark_complete() should flip completed from False to True."""
        task = Task(title="Morning walk", duration_minutes=30, priority="high")
        assert task.completed is False
        task.mark_complete()
        assert task.completed is True

    def test_mark_complete_is_idempotent(self):
        """Calling mark_complete() twice should leave completed as True."""
        task = Task(title="Feeding", duration_minutes=10)
        task.mark_complete()
        task.mark_complete()
        assert task.completed is True

    def test_is_high_priority_true(self):
        task = Task(title="Medication", duration_minutes=5, priority="high")
        assert task.is_high_priority() is True

    def test_is_high_priority_false_for_medium(self):
        task = Task(title="Playtime", duration_minutes=20, priority="medium")
        assert task.is_high_priority() is False


# ---------------------------------------------------------------------------
# Pet tests
# ---------------------------------------------------------------------------

class TestPet:
    def test_add_task_increases_count(self):
        """Adding a task should increase the pet's task count by 1."""
        pet = Pet(name="Biscuit", species="dog")
        assert len(pet.get_tasks()) == 0
        pet.add_task(Task("Morning walk", 30, priority="high"))
        assert len(pet.get_tasks()) == 1

    def test_add_multiple_tasks(self):
        """Adding N tasks should result in exactly N tasks stored."""
        pet = Pet(name="Mochi", species="cat")
        for i in range(3):
            pet.add_task(Task(f"Task {i}", 10))
        assert len(pet.get_tasks()) == 3

    def test_get_tasks_returns_copy(self):
        """get_tasks() should return a copy; mutating it should not affect the pet."""
        pet = Pet(name="Rex", species="dog")
        pet.add_task(Task("Walk", 20))
        tasks_copy = pet.get_tasks()
        tasks_copy.clear()
        assert len(pet.get_tasks()) == 1


# ---------------------------------------------------------------------------
# Owner tests
# ---------------------------------------------------------------------------

class TestOwner:
    def test_add_pet_increases_count(self):
        owner = Owner(name="Jordan")
        assert len(owner.get_pets()) == 0
        owner.add_pet(Pet(name="Biscuit", species="dog"))
        assert len(owner.get_pets()) == 1


# ---------------------------------------------------------------------------
# Scheduler tests
# ---------------------------------------------------------------------------

class TestScheduler:
    def _make_scheduler(self, available_minutes: int = 60) -> Scheduler:
        owner = Owner(name="Jordan", available_minutes=available_minutes)
        pet = Pet(name="Biscuit", species="dog")
        owner.add_pet(pet)
        pet.add_task(Task("Medication",  5, priority="high"))
        pet.add_task(Task("Feeding",    10, priority="high"))
        pet.add_task(Task("Walk",       30, priority="high"))
        pet.add_task(Task("Grooming",   40, priority="low"))
        return Scheduler(owner, pet)

    def test_high_priority_tasks_scheduled_first(self):
        """High-priority tasks should appear before low-priority tasks."""
        scheduler = self._make_scheduler(available_minutes=60)
        plan = scheduler.generate_plan()
        priorities = [t.priority for t in plan["scheduled"]]
        # No low-priority task should appear before any high-priority task
        last_high = max(
            (i for i, p in enumerate(priorities) if p == "high"), default=-1
        )
        first_low = min(
            (i for i, p in enumerate(priorities) if p == "low"), default=len(priorities)
        )
        assert last_high < first_low

    def test_tasks_fit_within_available_time(self):
        """Total scheduled duration must not exceed available_minutes."""
        scheduler = self._make_scheduler(available_minutes=60)
        plan = scheduler.generate_plan()
        total = sum(t.duration_minutes for t in plan["scheduled"])
        assert total <= 60

    def test_low_priority_task_skipped_when_no_time(self):
        """With tight time budget, the low-priority Grooming task should be skipped."""
        scheduler = self._make_scheduler(available_minutes=50)
        plan = scheduler.generate_plan()
        skipped_titles = [t.title for t in plan["skipped"]]
        assert "Grooming" in skipped_titles

    def test_all_tasks_scheduled_when_time_is_ample(self):
        """With plenty of time, no tasks should be skipped."""
        scheduler = self._make_scheduler(available_minutes=120)
        plan = scheduler.generate_plan()
        assert len(plan["skipped"]) == 0

    def test_explain_plan_contains_pet_name(self):
        """explain_plan() output should mention the pet's name."""
        scheduler = self._make_scheduler()
        plan = scheduler.generate_plan()
        explanation = scheduler.explain_plan(plan["scheduled"], plan["skipped"])
        assert "Biscuit" in explanation
