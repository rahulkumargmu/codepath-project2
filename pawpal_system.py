"""
pawpal_system.py — Backend logic layer for PawPal+.

Four core classes:
  - Task     : a single pet-care task (dataclass)
  - Pet      : a pet profile that holds a list of Tasks (dataclass)
  - Owner    : an owner profile that holds a list of Pets (dataclass)
  - Scheduler: generates and explains a daily care plan from an Owner + Pet
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Literal

PriorityLevel = Literal["low", "medium", "high"]

# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    """A single pet-care task with a duration and priority."""

    title: str
    duration_minutes: int
    priority: PriorityLevel = "medium"
    recurring: bool = False
    completed: bool = False
    notes: str = ""

    def is_high_priority(self) -> bool:
        """Return True if this task is marked high priority."""
        return self.priority == "high"

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    """A pet profile that owns a collection of care tasks."""

    name: str
    species: str
    breed: str = ""
    age_years: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return list(self.tasks)


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

@dataclass
class Owner:
    """An owner profile that holds preferences and a list of pets."""

    name: str
    available_minutes: int = 120
    preferred_start_time: str = "08:00"
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's roster."""
        self.pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return list(self.pets)


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    """
    Generates a daily care plan for a single pet.

    Algorithm sketch:
      1. Collect tasks from the pet.
      2. Sort by priority (high → medium → low), then by duration (shortest first).
      3. Greedily add tasks until available_minutes is exhausted.
      4. Return scheduled and skipped task lists.
    """

    PRIORITY_ORDER: dict[str, int] = {"high": 0, "medium": 1, "low": 2}

    def __init__(self, owner: Owner, pet: Pet) -> None:
        """Bind owner and pet; inherit available_minutes from the owner's preference."""
        self.owner = owner
        self.pet = pet
        self.available_minutes: int = owner.available_minutes

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate_plan(self) -> dict[str, list[Task]]:
        """Retrieve, sort, and filter the pet's tasks; return {"scheduled", "skipped"} dict."""
        tasks = self.pet.get_tasks()
        sorted_tasks = self.sort_tasks(tasks)
        scheduled, skipped = self.filter_tasks(sorted_tasks, self.available_minutes)
        return {"scheduled": scheduled, "skipped": skipped}

    def explain_plan(
        self,
        scheduled: list[Task],
        skipped: list[Task],
    ) -> str:
        """Return a formatted, time-slotted string explaining why tasks were scheduled or skipped."""
        try:
            start_dt = datetime.strptime(self.owner.preferred_start_time, "%H:%M")
        except ValueError:
            start_dt = datetime.strptime("08:00", "%H:%M")

        lines: list[str] = [
            f"Daily plan for {self.pet.name} ({self.pet.species})",
            f"Owner: {self.owner.name}  |  Available: {self.available_minutes} min  |  Start: {self.owner.preferred_start_time}",
            "",
        ]

        if scheduled:
            lines.append("Scheduled tasks:")
            current_dt = start_dt
            for task in scheduled:
                slot = current_dt.strftime("%H:%M")
                end_dt = current_dt + timedelta(minutes=task.duration_minutes)
                end_slot = end_dt.strftime("%H:%M")
                recurring_tag = " [recurring]" if task.recurring else ""
                lines.append(
                    f"  {slot}\u2013{end_slot}  {task.title} ({task.duration_minutes} min)"
                    f"  [priority: {task.priority}]{recurring_tag}"
                )
                if task.notes:
                    lines.append(f"             Note: {task.notes}")
                current_dt = end_dt
        else:
            lines.append("No tasks could be scheduled within the available time.")

        total_used = sum(t.duration_minutes for t in scheduled)
        lines.append(f"\nTotal time used: {total_used} / {self.available_minutes} min")

        if skipped:
            lines.append("\nSkipped tasks (insufficient time remaining):")
            for task in skipped:
                lines.append(
                    f"  - {task.title} ({task.duration_minutes} min, priority: {task.priority})"
                )

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority (high first), then by duration (shortest first) as a tiebreaker."""
        return sorted(
            tasks,
            key=lambda t: (self.PRIORITY_ORDER.get(t.priority, 99), t.duration_minutes),
        )

    def filter_tasks(
        self,
        tasks: list[Task],
        available_minutes: int,
    ) -> tuple[list[Task], list[Task]]:
        """Greedily pick tasks that fit in available_minutes; return (scheduled, skipped) tuple."""
        scheduled: list[Task] = []
        skipped: list[Task] = []
        remaining = available_minutes

        for task in tasks:
            if task.duration_minutes <= remaining:
                scheduled.append(task)
                remaining -= task.duration_minutes
            else:
                skipped.append(task)

        return scheduled, skipped
