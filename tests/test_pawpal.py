"""Tests for PawPal+ core behavior."""

import os
import sys
from datetime import date, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task


def make_pet(name="Mochi", **kwargs):
    """Helper to build a Pet with sensible defaults."""
    defaults = dict(
        birthday=date(2020, 1, 1),
        animal_type="cat",
        feeding_frequency=2,
    )
    defaults.update(kwargs)
    return Pet(name=name, **defaults)


# --- Task -----------------------------------------------------------------

def test_task_completion():
    """mark_complete() should change a task's status to completed."""
    task = Task(description="Feed Mochi")

    # A new task starts out not completed.
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_mark_incomplete():
    """mark_incomplete() should reset a completed task to not-done."""
    task = Task(description="Walk dog", completed=True)

    task.mark_incomplete()

    assert task.completed is False


def test_task_is_recurring():
    """is_recurring() is True for repeating tasks, False for one-time ones."""
    once = Task(description="Vet visit", frequency=Frequency.ONCE)
    daily = Task(description="Feeding", frequency=Frequency.DAILY)

    assert once.is_recurring() is False
    assert daily.is_recurring() is True


# --- Pet ------------------------------------------------------------------

def test_task_addition():
    """Adding a task to a Pet should increase that pet's task count."""
    pet = make_pet()

    # A new pet starts with no tasks.
    assert len(pet.tasks) == 0

    pet.add_task(Task(description="Feed Mochi"))

    assert len(pet.tasks) == 1


def test_task_removal():
    """Removing a task from a Pet should decrease its task count."""
    pet = make_pet()
    task = Task(description="Feed Mochi")
    pet.add_task(task)

    pet.remove_task(task)

    assert len(pet.tasks) == 0


def test_pet_pending_tasks():
    """pending_tasks() should exclude tasks already marked complete."""
    pet = make_pet()
    done = Task(description="Morning feed", completed=True)
    todo = Task(description="Evening feed")
    pet.add_task(done)
    pet.add_task(todo)

    pending = pet.pending_tasks()

    assert pending == [todo]


def test_pet_needs_medication():
    """needs_medication() reflects whether a medication is on record."""
    healthy = make_pet()
    treated = make_pet(medication="insulin")

    assert healthy.needs_medication() is False
    assert treated.needs_medication() is True


# --- Owner ----------------------------------------------------------------

def test_owner_all_and_pending_tasks():
    """Owner aggregates tasks across all pets and tracks pending ones."""
    owner = Owner(
        name="Kandi",
        birthday=date(1995, 5, 5),
        email="k@example.com",
        number="555-0100",
    )
    pet = make_pet()
    pet.add_task(Task(description="Feed", completed=True))
    pet.add_task(Task(description="Walk"))
    owner.add_pet(pet)

    assert len(owner.all_tasks()) == 2
    assert len(owner.pending_tasks()) == 1


# --- Scheduler ------------------------------------------------------------

def test_scheduler_next_task_picks_highest_priority():
    """next_task() returns the most urgent pending task."""
    scheduler = Scheduler()
    low = Task(description="Groom", priority_level=Priority.LOW)
    high = Task(description="Give meds", priority_level=Priority.HIGH)
    scheduler.add_task(low)
    scheduler.add_task(high)

    assert scheduler.next_task() is high


def test_scheduler_total_time_counts_only_pending():
    """total_time() sums durations of pending tasks only."""
    scheduler = Scheduler()
    scheduler.add_task(Task(description="Walk", duration=30))
    scheduler.add_task(Task(description="Feed", duration=10, completed=True))

    assert scheduler.total_time() == 30


def test_scheduler_organize_by_date():
    """organize_by_date() orders dated tasks first, undated last."""
    scheduler = Scheduler()
    later = Task(description="Later", due_date=date(2026, 7, 10), due_time=time(9, 0))
    sooner = Task(description="Sooner", due_date=date(2026, 7, 6), due_time=time(8, 0))
    undated = Task(description="Whenever")
    scheduler.add_task(later)
    scheduler.add_task(undated)
    scheduler.add_task(sooner)

    assert scheduler.organize_by_date() == [sooner, later, undated]
