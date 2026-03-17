- To run the app locally, use `uv run python main.py`.
- ALWAYS USE PARALLEL TOOLS WHEN APPLICABLE.
- The default branch in this repo is `main`.
- Use `main` or `origin/main` for diffs.
- Prefer automation: execute requested actions without confirmation unless blocked by missing info or safety/irreversibility.

## Style Guide

### General Principles

- Keep things in one function unless composable or reusable
- Avoid broad `try`/`except` where possible
- Avoid using `Any` unless unavoidable
- Prefer single word variable names where possible
- Use Python standard library APIs when possible, like `pathlib.Path`
- Rely on type inference when possible; avoid explicit type aliases or protocols unless necessary for exports or clarity
- Prefer functional iterables/comprehensions (`map`, comprehensions, `filter`) over verbose loops when readability stays clear

### Naming

Prefer single word names for variables and functions. Only use multiple words if necessary.

### Naming Enforcement (Read This)

THIS RULE IS MANDATORY FOR AGENT WRITTEN CODE.

- Use single word names by default for new locals, params, and helper functions.
- Multi-word names are allowed only when a single word would be unclear or ambiguous.
- Do not introduce new camelCase compounds when a short single-word alternative is clear.
- Before finishing edits, review touched lines and shorten newly introduced identifiers where possible.
- Good short names to prefer: `cfg`, `err`, `opts`, `path`, `root`, `child`, `state`, `timeout`.
- Examples to avoid unless truly required: `inputPID`, `existingClient`, `connectTimeout`, `workerPath`.

```py
# Good
foo = 1
def journal(path: str) -> None: ...

# Bad
foo_bar = 1
def prepare_journal(path: str) -> None: ...
```

Reduce total variable count by inlining when a value is only used once.

```py
# Good
data = Path(path).read_text(encoding="utf-8")

# Bad
journal_path = Path(path)
data = journal_path.read_text(encoding="utf-8")
```

### Destructuring

Avoid unnecessary unpacking. Use attribute/key access to preserve context.

```py
# Good
obj.a
obj.b

# Bad
a, b = obj.a, obj.b
```

### Variables

Prefer immutable patterns and avoid reassignment when possible.

```py
# Good
foo = 1 if condition else 2

# Bad
foo = None
if condition:
    foo = 1
else:
    foo = 2
```

### Control Flow

Avoid `else` statements. Prefer early returns.

```py
# Good
def foo() -> int:
    if condition:
        return 1
    return 2

# Bad
def foo() -> int:
    if condition:
        return 1
    else:
        return 2
```



## Testing

- Avoid mocks as much as possible
- Test actual implementation, do not duplicate logic into tests
- Run tests from repo root with `uv run pytest`; use node ids for single tests like `uv run pytest tests/test_example.py::test_name -q`.

## Type Checking

- Always run `uv run mypy .` when type checking is enabled; do not call internal mypy modules directly.
