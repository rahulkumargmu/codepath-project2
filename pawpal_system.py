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
    notes: str = ""

    def is_high_priority(self) -> bool:
        """Return True if this task is marked high priority."""
        pass


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
        pass

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        pass


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
        pass

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        pass


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
        self.owner = owner
        self.pet = pet
        self.available_minutes: int = owner.available_minutes

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate_plan(self) -> dict[str, list[Task]]:
        """
        Build and return a daily plan.

        Returns:
            {"scheduled": [...], "skipped": [...]}
        """
        pass

    def explain_plan(
        self,
        scheduled: list[Task],
        skipped: list[Task],
    ) -> str:
        """
        Produce a human-readable explanation of why tasks were included or
        skipped in the generated plan.
        """
        pass

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """
        Return tasks sorted by priority (high first), then duration
        (shortest first) as a tiebreaker.
        """
        pass

    def filter_tasks(
        self,
        tasks: list[Task],
        available_minutes: int,
    ) -> tuple[list[Task], list[Task]]:
        """
        Greedily select tasks that fit within available_minutes.

        Returns:
            (scheduled, skipped) tuple of task lists.
        """
        pass
