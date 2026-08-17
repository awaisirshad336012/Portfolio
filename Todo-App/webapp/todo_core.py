"""
Core To-Do logic — no input()/print() here on purpose.
This module only manipulates data and files, so it can be reused by
both the interactive menu (todo.py) and the argparse CLI (todo_cli.py),
and can be tested directly without simulating user input.
"""

import json
import os
import tempfile
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

VALID_PRIORITIES = ("Low", "Medium", "High")
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def load_tasks(filepath=TASKS_FILE):
    """Load tasks from the JSON file. Returns empty list if file doesn't exist or is corrupt."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_tasks(tasks, filepath=TASKS_FILE):
    """
    Save the tasks list to the JSON file, atomically.
    We write to a temp file first, then rename it over the real file.
    On virtually every OS, a rename is atomic — so even if the program
    crashes or the machine loses power mid-write, tasks.json is either
    the old complete version or the new complete version, never a
    half-written, corrupted file.
    """
    directory = os.path.dirname(filepath) or "."
    fd, temp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(tasks, f, indent=4)
        os.replace(temp_path, filepath)
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise


def add_task(tasks, description, priority="Medium", due_date=None):
    """
    Add a new task to the tasks list (in place) and return it.
    Raises ValueError on bad input instead of printing — callers decide how to show errors.
    """
    description = description.strip()
    if not description:
        raise ValueError("Task description cannot be empty.")

    priority = priority.capitalize()
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Priority must be one of {VALID_PRIORITIES}.")

    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format.")

    new_id = (max((t["id"] for t in tasks), default=0)) + 1
    task = {
        "id": new_id,
        "task": description,
        "done": False,
        "priority": priority,
        "due_date": due_date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": None,
    }
    tasks.append(task)
    return task


def get_sorted_tasks(tasks, sort_by="id", show_done=True):
    """
    Return a NEW sorted/filtered list — never mutates the original.
    sort_by: 'id', 'priority', or 'due_date'
    """
    result = tasks if show_done else [t for t in tasks if not t["done"]]

    if sort_by == "priority":
        return sorted(result, key=lambda t: PRIORITY_ORDER.get(t.get("priority", "Medium"), 1))
    elif sort_by == "due_date":
        # Tasks with no due date sort to the end
        return sorted(result, key=lambda t: (t.get("due_date") is None, t.get("due_date")))
    return sorted(result, key=lambda t: t["id"])


def find_task(tasks, task_id):
    """Return the task dict with this id, or None."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def mark_complete(tasks, task_id):
    """Mark a task as done and record when. Returns True if found, False otherwise."""
    task = find_task(tasks, task_id)
    if task is None:
        return False
    task["done"] = True
    task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return True


def toggle_complete(tasks, task_id):
    """
    Flip a task's done status. Marking done records completed_at;
    un-marking clears it. Returns True if found, False otherwise.
    """
    task = find_task(tasks, task_id)
    if task is None:
        return False
    task["done"] = not task["done"]
    task["completed_at"] = (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S") if task["done"] else None
    )
    return True


def delete_task(tasks, task_id):
    """Remove a task by id. Returns True if found and removed, False otherwise."""
    task = find_task(tasks, task_id)
    if task is None:
        return False
    tasks.remove(task)
    return True
