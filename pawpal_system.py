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
from datetime import date
from typing import List, Optional


@dataclass
class Owner:
    """Holds the owner's personal info."""

    name: str
    birthday: date
    email: str
    number: str

    # Owns one or more pets and has a scheduler.
    pets: List["Pet"] = field(default_factory=list)
    scheduler: Optional["Scheduler"] = None


@dataclass
class Pet:
    """Holds a pet's basic info and care needs."""

    name: str
    birthday: date
    animal_type: str
    feeding_frequency: int  # times per day
    medication: Optional[str] = None

    # Tasks this pet requires (feeding, meds, grooming, etc.).
    tasks: List["Task"] = field(default_factory=list)


@dataclass
class Task:
    """A single pet care task."""

    description: str
    priority_level: int
    duration: int = 0  # minutes the task takes

    def add_daily_task(self, task: "Task") -> None:
        """Add a task to the daily list."""
        raise NotImplementedError

    def remove_daily_task(self, task: "Task") -> None:
        """Remove a task from the daily list."""
        raise NotImplementedError

    def add_monthly_task(self, task: "Task") -> None:
        """Add a task to the monthly list."""
        raise NotImplementedError

    def remove_monthly_task(self, task: "Task") -> None:
        """Remove a task from the monthly list."""
        raise NotImplementedError


class Scheduler:
    """Builds and organizes an owner's care schedule."""

    def __init__(self, grooming_frequency: int = 0, walk_frequency: int = 0) -> None:
        self.schedule: List[Task] = []
        self.grooming_frequency = grooming_frequency  # times per month
        self.walk_frequency = walk_frequency  # times per day

    def organize_by_date(self) -> List[Task]:
        """Order the schedule by date."""
        raise NotImplementedError

    def organize_by_priority(self) -> List[Task]:
        """Order the schedule by task priority level."""
        raise NotImplementedError
