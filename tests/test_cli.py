from todo_cli.cli import main


def test_add_and_list(tmp_path, capsys):
    store = tmp_path / "tasks.json"

    assert main(["--store", str(store), "add", "buy milk"]) == 0
    out = capsys.readouterr().out
    assert "added 1: buy milk" in out

    assert main(["--store", str(store), "list"]) == 0
    out = capsys.readouterr().out
    assert "[ ] 1. buy milk" in out


def test_done_and_rm(tmp_path, capsys):
    store = tmp_path / "tasks.json"

    main(["--store", str(store), "add", "one"])
    main(["--store", str(store), "add", "two"])
    capsys.readouterr()

    main(["--store", str(store), "done", "1"])
    main(["--store", str(store), "list"])
    out = capsys.readouterr().out
    assert "[x] 1. one" in out
    assert "[ ] 2. two" in out

    main(["--store", str(store), "rm", "1"])
    capsys.readouterr()
    main(["--store", str(store), "list"])
    out = capsys.readouterr().out
    assert "one" not in out
    assert "[ ] 2. two" in out


def test_list_empty(tmp_path, capsys):
    store = tmp_path / "tasks.json"
    main(["--store", str(store), "list"])
    out = capsys.readouterr().out
    assert "(no tasks)" in out
