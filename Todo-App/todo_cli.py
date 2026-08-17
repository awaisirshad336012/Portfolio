"""
Professional command-line interface using argparse, e.g.:
    python todo_cli.py add "Buy milk" --priority High --due 2026-08-20
    python todo_cli.py list --sort priority
    python todo_cli.py done 1
    python todo_cli.py delete 2

Reuses the exact same todo_core logic as the interactive menu (todo.py) —
zero duplicated business logic between the two interfaces.
"""

import argparse

from todo_core import (
    load_tasks,
    save_tasks,
    add_task,
    get_sorted_tasks,
    mark_complete,
    delete_task,
)


def cmd_add(args):
    tasks = load_tasks()
    try:
        task = add_task(tasks, args.description, args.priority, args.due)
    except ValueError as e:
        print(f"Error: {e}")
        return
    save_tasks(tasks)
    print(f"Task added with ID {task['id']}")


def cmd_list(args):
    tasks = load_tasks()
    sorted_tasks = get_sorted_tasks(tasks, sort_by=args.sort, show_done=not args.pending_only)

    if not sorted_tasks:
        print("No tasks found.")
        return

    for task in sorted_tasks:
        status = "Done" if task["done"] else "Pending"
        due = task.get("due_date") or "no due date"
        print(f"[{task['id']}] {task['task']} - {status} | Priority: {task['priority']} | Due: {due}")


def cmd_done(args):
    tasks = load_tasks()
    if mark_complete(tasks, args.id):
        save_tasks(tasks)
        print(f"Task {args.id} marked as complete.")
    else:
        print(f"No task found with ID {args.id}.")


def cmd_delete(args):
    tasks = load_tasks()
    if delete_task(tasks, args.id):
        save_tasks(tasks)
        print(f"Task {args.id} deleted.")
    else:
        print(f"No task found with ID {args.id}.")


def build_parser():
    parser = argparse.ArgumentParser(prog="todo", description="A simple command-line to-do manager.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument("--priority", choices=["Low", "Medium", "High"], default="Medium")
    add_parser.add_argument("--due", help="Due date in YYYY-MM-DD format")
    add_parser.set_defaults(func=cmd_add)

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--sort", choices=["id", "priority", "due_date"], default="id")
    list_parser.add_argument("--pending-only", action="store_true", help="Hide completed tasks")
    list_parser.set_defaults(func=cmd_list)

    done_parser = subparsers.add_parser("done", help="Mark a task as complete")
    done_parser.add_argument("id", type=int, help="Task ID")
    done_parser.set_defaults(func=cmd_done)

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")
    delete_parser.set_defaults(func=cmd_delete)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
