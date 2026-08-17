"""
Flask web UI for the To-Do App.
Reuses the exact same todo_core.py logic as the interactive menu (todo.py)
and the argparse CLI (todo_cli.py) — same tasks.json, three interfaces.
"""

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

from todo_core import (
    load_tasks,
    save_tasks,
    add_task,
    get_sorted_tasks,
    toggle_complete,
    delete_task,
)

app = Flask(__name__)


def format_dt(dt_string):
    """Turn '2026-08-17 15:24:00' into a friendly 'Aug 17, 3:24 PM'. Returns None as-is."""
    if not dt_string:
        return None
    dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
    formatted = dt.strftime("%b %d, %I:%M %p")
    # Strip a leading zero from the hour (e.g. "03:24 PM" -> "3:24 PM") portably
    return formatted.replace(" 0", " ")


def with_display_fields(tasks):
    """
    Build display copies of tasks with friendly timestamps, WITHOUT touching
    the real stored data — the raw created_at/completed_at stay untouched
    in tasks.json for anything else (CLI, tests) that reads them.
    """
    display_tasks = []
    for task in tasks:
        display_task = dict(task)
        display_task["created_display"] = format_dt(task.get("created_at"))
        display_task["completed_display"] = format_dt(task.get("completed_at"))
        display_tasks.append(display_task)
    return display_tasks


@app.route("/")
def index():
    tasks = load_tasks()
    sort_by = request.args.get("sort", "id")
    pending_only = request.args.get("pending_only") == "1"

    sorted_tasks = get_sorted_tasks(tasks, sort_by=sort_by, show_done=not pending_only)

    return render_template(
        "index.html",
        tasks=with_display_fields(sorted_tasks),
        sort_by=sort_by,
        pending_only=pending_only,
        total=len(tasks),
        done_count=len([t for t in tasks if t["done"]]),
    )


@app.route("/add", methods=["POST"])
def add():
    tasks = load_tasks()
    description = request.form.get("description", "")
    priority = request.form.get("priority", "Medium")
    due_date = request.form.get("due_date") or None

    try:
        add_task(tasks, description, priority, due_date)
        save_tasks(tasks)
    except ValueError:
        pass  # silently ignore bad input for this simple bonus UI

    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete(task_id):
    tasks = load_tasks()
    toggle_complete(tasks, task_id)
    save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    tasks = load_tasks()
    delete_task(tasks, task_id)
    save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
