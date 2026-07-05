"""PawPal+ data models and scheduling logic (skeleton).

Generated from diagrams/uml_draft.mmd. Method bodies are left as stubs for
you to implement.

Note on getters/setters: the UML lists explicit get/set methods for each
attribute. In Python, dataclass fields are already public attributes, so you
normally read/write them directly (e.g. `pet.name = "Mochi"`) instead of
writing boilerplate accessors. The stubs below follow that Pythonic style.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time
from enum import IntEnum
from typing import List, Optional


class Priority(IntEnum):
    """How urgent a task is (higher value = more urgent)."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Frequency(IntEnum):
    """How often a task repeats."""

    ONCE = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3


@dataclass
class Owner:
    """Holds the owner's personal info and manages their pets."""

    name: str
    birthday: date
    email: str
    number: str

    # Owns one or more pets and has a scheduler.
    pets: List["Pet"] = field(default_factory=list)
    scheduler: Optional["Scheduler"] = None

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: "Pet") -> None:
        """Remove a pet from this owner (no error if it isn't there)."""
        if pet in self.pets:
            self.pets.remove(pet)

    def all_tasks(self) -> List["Task"]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def pending_tasks(self) -> List["Task"]:
        """Return every not-yet-completed task across all pets."""
        return [task for task in self.all_tasks() if not task.completed]

    def __str__(self) -> str:
        """Return a one-line summary of the owner and their task load."""
        return (
            f"{self.name} — {len(self.pets)} pet(s), "
            f"{len(self.all_tasks())} task(s), "
            f"{len(self.pending_tasks())} pending"
        )


@dataclass
class Pet:
    """Holds a pet's basic info, care needs, and the tasks it requires."""

    name: str
    birthday: date
    animal_type: str
    feeding_frequency: int  # times per day
    medication: Optional[str] = None

    # Tasks this pet requires (feeding, meds, grooming, etc.).
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Detach a care task from this pet (no error if it isn't there)."""
        if task in self.tasks:
            self.tasks.remove(task)

    def pending_tasks(self) -> List["Task"]:
        """Return the tasks that still need to be done."""
        return [task for task in self.tasks if not task.completed]

    def needs_medication(self) -> bool:
        """Return True if this pet has a medication on record."""
        return self.medication is not None

    def __str__(self) -> str:
        """Return a one-line summary of the pet, its care needs, and tasks."""
        meds = self.medication if self.medication else "none"
        return (
            f"{self.name} ({self.animal_type}) — "
            f"fed {self.feeding_frequency}x/day, meds: {meds}, "
            f"{len(self.tasks)} task(s), {len(self.pending_tasks())} pending"
        )


@dataclass
class Task:
    """A single pet care activity (feeding, meds, a walk, grooming, etc.).

    A task describes *what* to do, *how long* it takes, *how often* it repeats,
    *how urgent* it is, and *whether it has been done*.
    """

    description: str
    duration: int = 0  # minutes the task takes
    frequency: Frequency = Frequency.ONCE
    priority_level: Priority = Priority.MEDIUM
    completed: bool = False

    # When the task is due: which day and what time of day it must be done.
    # (used by the Scheduler to order things).
    due_date: Optional[date] = None
    due_time: Optional[time] = None

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Reset this task to not-yet-done (e.g. when it recurs)."""
        self.completed = False

    def is_recurring(self) -> bool:
        """Return True if the task repeats rather than happening only once."""
        return self.frequency != Frequency.ONCE

    def __str__(self) -> str:
        """Return a one-line summary of the task and its status."""
        status = "✓" if self.completed else "✗"
        when = f", due {self.due_time.strftime('%H:%M')}" if self.due_time else ""
        return (
            f"[{status}] {self.description} "
            f"({self.duration} min, {self.frequency.name.lower()}, "
            f"priority {self.priority_level.name.lower()}{when})"
        )


class Scheduler:
    """The "brain" that retrieves, organizes, and manages tasks across pets."""

    def __init__(self, grooming_frequency: int = 0, walk_frequency: int = 0) -> None:
        """Create an empty scheduler with grooming/walk frequency settings."""
        self.schedule: List[Task] = []
        self.grooming_frequency = grooming_frequency  # times per month
        self.walk_frequency = walk_frequency  # times per day

    # --- retrieve ---------------------------------------------------------

    def build_schedule(self, owner: "Owner") -> List[Task]:
        """Pull every task from all of the owner's pets into the schedule."""
        self.schedule = owner.all_tasks()
        return self.schedule

    def add_task(self, task: Task) -> None:
        """Add a single task to the schedule."""
        self.schedule.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule (no error if it isn't there)."""
        if task in self.schedule:
            self.schedule.remove(task)

    # --- organize ---------------------------------------------------------

    def organize_by_date(self) -> List[Task]:
        """Return the schedule ordered by due date then time (undated last)."""
        return sorted(
            self.schedule,
            key=lambda task: (
                task.due_date is None,
                task.due_date or date.max,
                task.due_time or time.max,
            ),
        )

    def organize_by_priority(self) -> List[Task]:
        """Return the schedule ordered by priority, most urgent first."""
        return sorted(
            self.schedule,
            key=lambda task: task.priority_level,
            reverse=True,
        )

    # --- manage -----------------------------------------------------------

    def pending_tasks(self) -> List[Task]:
        """Return the tasks in the schedule that still need to be done."""
        return [task for task in self.schedule if not task.completed]

    def next_task(self) -> Optional[Task]:
        """Return the most urgent pending task, or None if all are done."""
        pending = self.pending_tasks()
        if not pending:
            return None
        return max(pending, key=lambda task: task.priority_level)

    def total_time(self) -> int:
        """Return the total minutes needed for all pending tasks."""
        return sum(task.duration for task in self.pending_tasks())
