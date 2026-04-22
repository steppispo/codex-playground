"""Core todo-list data model and persistence."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


@dataclass
class TodoList:
    tasks: list[Task] = field(default_factory=list)

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("title must not be empty")
        next_id = 1 + max((t.id for t in self.tasks), default=0)
        task = Task(id=next_id, title=title)
        self.tasks.append(task)
        return task

    def complete(self, task_id: int) -> Task:
        task = self._get(task_id)
        task.done = True
        return task

    def remove(self, task_id: int) -> Task:
        task = self._get(task_id)
        self.tasks.remove(task)
        return task

    def pending(self) -> list[Task]:
        return [t for t in self.tasks if not t.done]

    def _get(self, task_id: int) -> Task:
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise KeyError(f"no task with id={task_id}")

    def to_dict(self) -> dict:
        return {"tasks": [asdict(t) for t in self.tasks]}

    @classmethod
    def from_dict(cls, data: dict) -> TodoList:
        tasks = [Task(**t) for t in data.get("tasks", [])]
        return cls(tasks=tasks)


def load(path: Path) -> TodoList:
    if not path.exists():
        return TodoList()
    return TodoList.from_dict(json.loads(path.read_text()))


def save(todo: TodoList, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(todo.to_dict(), indent=2))
