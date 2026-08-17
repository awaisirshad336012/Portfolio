"""
Interactive menu interface for the To-Do App.
All actual logic lives in todo_core.py — this file only handles
user input/output.
"""

from todo_core import (
    load_tasks,
    save_tasks,
    add_task,
    get_sorted_tasks,
    mark_complete,
    delete_task,
    VALID_PRIORITIES,
)


def prompt_add_task(tasks):
    description = input("Enter task description: ")

    priority = input(f"Priority {VALID_PRIORITIES} [default: Medium]: ").strip() or "Medium"
    due_date = input("Due date YYYY-MM-DD (optional, press Enter to skip): ").strip() or None

    try:
        task = add_task(tasks, description, priority, due_date)
    except ValueError as e:
        print(f"Error: {e}")
        return

    save_tasks(tasks)
    print(f"Task added with ID {task['id']}")


def prompt_list_tasks(tasks):
    if not tasks:
        print("No tasks yet. Add one!")
        return

    sort_choice = input("Sort by (id/priority/due_date) [default: id]: ").strip() or "id"
    show_done_input = input("Show completed tasks too? (y/n) [default: y]: ").strip().lower()
    show_done = show_done_input != "n"

    sorted_tasks = get_sorted_tasks(tasks, sort_by=sort_choice, show_done=show_done)

    if not sorted_tasks:
        print("No tasks match that filter.")
        return

    print("\n--- YOUR TASKS ---")
    for task in sorted_tasks:
        status = "Done" if task["done"] else "Pending"
        due = task.get("due_date") or "no due date"
        print(f"[{task['id']}] {task['task']} - {status} | Priority: {task['priority']} | Due: {due}")


def prompt_mark_complete(tasks):
    if not tasks:
        print("No tasks to update.")
        return

    try:
        task_id = int(input("Enter task ID to mark complete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    if mark_complete(tasks, task_id):
        save_tasks(tasks)
        print(f"Task {task_id} marked as complete.")
    else:
        print(f"No task found with ID {task_id}.")


def prompt_delete_task(tasks):
    if not tasks:
        print("No tasks to delete.")
        return

    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    if delete_task(tasks, task_id):
        save_tasks(tasks)
        print(f"Task {task_id} deleted.")
    else:
        print(f"No task found with ID {task_id}.")


def main():
    tasks = load_tasks()

    while True:
        print("\n===== TO-DO APP =====")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task Complete")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            prompt_add_task(tasks)
        elif choice == "2":
            prompt_list_tasks(tasks)
        elif choice == "3":
            prompt_mark_complete(tasks)
        elif choice == "4":
            prompt_delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
