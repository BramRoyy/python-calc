# python-calc

Desktop calculator POC built with Python and CustomTkinter.

## Requirements

- Python 3.14
- `uv`

## Setup

Install all dependencies:

```bash
uv sync --all-groups
```

## Run App

```bash
uv run python main.py
```

The window title is `Python Calc (POC)`.

## Test

Run default tests (fast path, excludes E2E by default):

```bash
uv run pytest -q
```

Run E2E tests explicitly:

```bash
uv run pytest -m e2e -q
```

Notes for E2E:
- E2E requires Windows interactive desktop session.
- E2E may be skipped if pywinauto cannot attach the app window in current session.

## Project Layout

- `main.py`: calculator app, state flow, safe AST evaluator.
- `tests/test_calc.py`: evaluator and formatter unit tests.
- `tests/test_state.py`: state transition unit tests.
- `tests/e2e/test_calculator_e2e.py`: pywinauto E2E flow tests.
- `pytest.ini`: pytest marker and default selection config.

## Git Notes

- `.tmp/` is ignored and should not be committed.
