import pytest

from todo_cli.core import TodoList, load, save


def test_add_assigns_incrementing_ids():
    todo = TodoList()
    a = todo.add("first")
    b = todo.add("second")
    assert (a.id, b.id) == (1, 2)
    assert [t.title for t in todo.tasks] == ["first", "second"]


def test_add_rejects_empty_title():
    todo = TodoList()
    with pytest.raises(ValueError):
        todo.add("   ")


def test_complete_marks_task_done():
    todo = TodoList()
    todo.add("write tests")
    todo.complete(1)
    assert todo.tasks[0].done is True
    assert todo.pending() == []


def test_complete_unknown_id_raises():
    todo = TodoList()
    with pytest.raises(KeyError):
        todo.complete(42)


def test_remove_drops_task():
    todo = TodoList()
    todo.add("a")
    todo.add("b")
    todo.remove(1)
    assert [t.title for t in todo.tasks] == ["b"]


def test_roundtrip_save_load(tmp_path):
    path = tmp_path / "nested" / "tasks.json"
    todo = TodoList()
    todo.add("persist me")
    todo.complete(1)
    save(todo, path)

    loaded = load(path)
    assert len(loaded.tasks) == 1
    assert loaded.tasks[0].title == "persist me"
    assert loaded.tasks[0].done is True


def test_load_missing_file_returns_empty(tmp_path):
    todo = load(tmp_path / "missing.json")
    assert todo.tasks == []
