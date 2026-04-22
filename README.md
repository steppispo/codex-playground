# codex-playground

A tiny Python CLI todo-list app, used as a sandbox for testing OpenAI Codex
features (refactors, multi-file edits, test generation, etc.).

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
todo add "write the README"
todo add "ship a PR"
todo list
todo done 1
todo rm 2
```

Tasks are stored by default at `~/.todo_cli/tasks.json`. Override with
`--store path/to/file.json`.

## Development

```bash
pytest               # run tests
ruff check .         # lint
ruff format .        # format
```

CI runs lint, format check, and tests on Python 3.10, 3.11, and 3.12 via
GitHub Actions (`.github/workflows/ci.yml`).

## Project layout

```
src/todo_cli/
  __init__.py
  core.py      # TodoList / Task data model + JSON persistence
  cli.py       # argparse-based command-line interface
tests/
  test_core.py
  test_cli.py
```

## Ideas for Codex to try

- Add a `todo edit <id> <new title>` subcommand.
- Add due dates / priorities to tasks.
- Swap JSON persistence for SQLite.
- Add colorized output with `rich`.
- Add a `--json` flag to `list` for machine-readable output.
