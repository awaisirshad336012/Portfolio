"""
Unit tests for todo_core.py.

Run with:  pytest test_todo.py -v

Notice tests call add_task/mark_complete/etc directly — this is only
possible because todo_core.py doesn't call input()/print() itself.
That separation is what makes the logic testable.
"""

import pytest
from todo_core import (
    add_task,
    get_sorted_tasks,
    find_task,
    mark_complete,
    delete_task,
)


@pytest.fixture
def tasks():
    """A fresh empty task list for every test."""
    return []


def test_add_task_creates_task_with_correct_fields(tasks):
    task = add_task(tasks, "Buy milk", priority="High", due_date="2026-12-01")
    assert task["task"] == "Buy milk"
    assert task["priority"] == "High"
    assert task["due_date"] == "2026-12-01"
    assert task["done"] is False
    assert len(tasks) == 1


def test_add_task_assigns_incrementing_ids(tasks):
    t1 = add_task(tasks, "First task")
    t2 = add_task(tasks, "Second task")
    assert t1["id"] == 1
    assert t2["id"] == 2


def test_add_task_rejects_empty_description(tasks):
    with pytest.raises(ValueError):
        add_task(tasks, "   ")


def test_add_task_rejects_invalid_priority(tasks):
    with pytest.raises(ValueError):
        add_task(tasks, "Task", priority="Urgent")


def test_add_task_rejects_bad_due_date_format(tasks):
    with pytest.raises(ValueError):
        add_task(tasks, "Task", due_date="12/01/2026")


def test_find_task_returns_none_when_missing(tasks):
    add_task(tasks, "Only task")
    assert find_task(tasks, 999) is None


def test_mark_complete_updates_status(tasks):
    task = add_task(tasks, "Finish report")
    assert task["done"] is False
    assert mark_complete(tasks, task["id"]) is True
    assert task["done"] is True


def test_mark_complete_returns_false_for_missing_id(tasks):
    assert mark_complete(tasks, 42) is False


def test_delete_task_removes_it(tasks):
    task = add_task(tasks, "Temporary task")
    assert delete_task(tasks, task["id"]) is True
    assert len(tasks) == 0


def test_delete_task_returns_false_for_missing_id(tasks):
    add_task(tasks, "Some task")
    assert delete_task(tasks, 999) is False


def test_get_sorted_tasks_by_priority(tasks):
    add_task(tasks, "Low prio", priority="Low")
    add_task(tasks, "High prio", priority="High")
    add_task(tasks, "Medium prio", priority="Medium")

    sorted_tasks = get_sorted_tasks(tasks, sort_by="priority")
    assert [t["priority"] for t in sorted_tasks] == ["High", "Medium", "Low"]


def test_get_sorted_tasks_hides_done_when_requested(tasks):
    t1 = add_task(tasks, "Task 1")
    add_task(tasks, "Task 2")
    mark_complete(tasks, t1["id"])

    pending_only = get_sorted_tasks(tasks, show_done=False)
    assert len(pending_only) == 1
    assert pending_only[0]["task"] == "Task 2"


def test_get_sorted_tasks_does_not_mutate_original_list(tasks):
    add_task(tasks, "B task", priority="Low")
    add_task(tasks, "A task", priority="High")

    original_order = [t["id"] for t in tasks]
    get_sorted_tasks(tasks, sort_by="priority")

    assert [t["id"] for t in tasks] == original_order
