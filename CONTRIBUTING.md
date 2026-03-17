# Contributing to python-calc

Thanks for contributing. This project is intentionally small, so we value focused, minimal changes that keep the workflow simple.

Commonly accepted contributions:

- Bug fixes
- Test improvements
- Lint/format consistency updates
- Documentation improvements
- Small developer-experience improvements

If your change is large or introduces a new feature direction, open an issue first so scope is clear before implementation.

## Developing python-calc

This repository is `uv`-first.

- Python requirement: `>=3.14`
- Recommended interpreter target: `.python-version` (`3.14`)
- Package/environment manager: `uv`

Do not switch tooling (`pipenv`, `poetry`, `pip-tools`) unless explicitly requested by maintainers.

### Setup (uv-first)

Run all commands from repository root.

Bootstrap environment:

```bash
uv sync
```

If dependency groups are added:

```bash
uv sync --group dev
uv sync --all-groups
```

Dependency management:

```bash
uv add <package>
uv add --dev <package>
uv remove <package>
uv lock
```

Interpreter pinning (if needed):

```bash
uv python pin 3.14
```

## Build, Lint, and Test

Use `uv run` for project commands.

### Run app

```bash
uv run python main.py
```

If module entrypoints are added later:

```bash
uv run python -m <module>
```

### Lint and format

```bash
uv run ruff check .
uv run ruff check . --fix
uv run ruff format .
uv run ruff format --check .
```

If project opts into Black instead:

```bash
uv run black --check .
```

### Type checking

```bash
uv run mypy .
uv run pyright
```

Run only tools configured by the repository at that time.

### Tests

```bash
uv run pytest -q
uv run pytest -vv
uv run pytest -x
uv run pytest --lf
```

### Running a single test (important)

```bash
# Single test file
uv run pytest tests/test_example.py -q

# Single test function
uv run pytest tests/test_example.py::test_happy_path -q

# Single test class
uv run pytest tests/test_example.py::TestCalculator -q

# Specific parametrized case
uv run pytest tests/test_example.py::test_addition[ints] -q

# Keyword expression
uv run pytest -k "happy_path and not slow" -q
```

## Pull Request Expectations

- Keep PRs small and focused.
- Explain what changed and why.
- Include validation details (commands run, tests executed).
- Add or update tests for behavior changes.
- Avoid unrelated refactors in bug-fix PRs.

## Agent and Style Rules

Agent-specific policies and coding rules are documented in `AGENTS.md`.

If there is any conflict:

1. Explicit user instruction
2. `AGENTS.md`
3. `CONTRIBUTING.md`
