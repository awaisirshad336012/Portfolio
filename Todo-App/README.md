# To-Do App (Flask)

A simple to-do list web app built with Python and Flask. Tasks are saved in a `tasks.json` file, so your list stays there even after you close the app.

## Features

- Add tasks with a priority (High / Medium / Low) and an optional due date
- Mark tasks as complete
- Delete tasks
- Sort tasks by id, priority, or due date
- View all tasks or hide the ones already completed
- Data is stored locally in `tasks.json`, no database needed

## Project Structure

```
todo-app/
│
├── webapp/
│   ├── app.py            # Flask app (routes + web UI)
│   └── templates/
│       └── index.html    # Front-end page
│
├── todo_core.py           # Core logic (add, sort, mark complete, delete, etc.)
├── todo.py                 # Interactive command-line version of the app
├── todo_cli.py              # Command-line interface helpers
├── test_todo.py             # Unit tests (pytest)
└── tasks.json                # Where tasks get saved
```

The idea behind the structure: `todo_core.py` has all the actual logic, and everything else (the CLI, the Flask app, the tests) just calls into that file. This keeps the logic testable and separate from the input/output layer.

## How to Run

1. Install dependencies:
   ```
   pip install flask pytest
   ```

2. Run the web app:
   ```
   cd webapp
   python app.py
   ```

3. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Running the CLI Version

If you'd rather use it from the terminal instead of the browser:
```
python todo.py
```

## Running Tests

```
pytest test_todo.py -v
```

## Notes

This project was built as part of my Python/Flask practice while learning full-stack development.
