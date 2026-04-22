"""Command-line interface for the todo list."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import TodoList, load, save

DEFAULT_STORE = Path.home() / ".todo_cli" / "tasks.json"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="todo", description="A tiny todo-list CLI.")
    p.add_argument(
        "--store",
        type=Path,
        default=DEFAULT_STORE,
        help=f"Path to the tasks JSON file (default: {DEFAULT_STORE}).",
    )
    sub = p.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Add a new task.")
    add.add_argument("title", help="Task title.")

    sub.add_parser("list", help="List all tasks.")

    done = sub.add_parser("done", help="Mark a task as complete.")
    done.add_argument("task_id", type=int)

    rm = sub.add_parser("rm", help="Remove a task.")
    rm.add_argument("task_id", type=int)

    return p


def _render(todo: TodoList) -> str:
    if not todo.tasks:
        return "(no tasks)"
    lines = []
    for t in todo.tasks:
        marker = "x" if t.done else " "
        lines.append(f"[{marker}] {t.id}. {t.title}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    todo = load(args.store)

    if args.command == "add":
        task = todo.add(args.title)
        save(todo, args.store)
        print(f"added {task.id}: {task.title}")
    elif args.command == "list":
        print(_render(todo))
    elif args.command == "done":
        task = todo.complete(args.task_id)
        save(todo, args.store)
        print(f"completed {task.id}: {task.title}")
    elif args.command == "rm":
        task = todo.remove(args.task_id)
        save(todo, args.store)
        print(f"removed {task.id}: {task.title}")
    else:  # pragma: no cover - argparse enforces this
        parser.error(f"unknown command: {args.command}")

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
