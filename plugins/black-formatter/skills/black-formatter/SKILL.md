---
name: black-formatter
description: This skill should be used when the user asks to "format python code", "run black", "format with black", "fix formatting", or when editing/writing Python files in a project that uses Black for formatting.
version: 1.0.0
---

# Black Formatter

Formats Python code using Black, the uncompromising code formatter.

## When This Skill Applies

- User asks to format Python code or run Black
- After writing/editing Python files in a repo with a `pyproject.toml` `[tool.black]` section or existing Black usage (check `pyproject.toml`, CI config, pre-commit config)
- User asks to fix inconsistent formatting in `.py` files

## Detecting Black Usage

Check for any of:
- `[tool.black]` in `pyproject.toml`
- `black` in `requirements*.txt`, `pyproject.toml` dev deps, or `.pre-commit-config.yaml`

## Running Black

Format a file or directory in place:

```bash
black path/to/file.py
black .
```

Check formatting without writing changes (useful before committing):

```bash
black --check --diff path/to/file.py
```

Respect project config automatically — Black reads `[tool.black]` from `pyproject.toml` if present (line-length, target-version, exclude patterns, etc). Don't override those settings with flags unless the user asks.

## Recommended Configuration

If Black is used but no `[tool.black]` section exists yet, offer (don't auto-apply) this baseline as a starting point — confirm with the user before writing it:

```toml
[tool.black]
line-length = 100
target-version = ["py<repo's minimum supported version>"]
```

`line-length = 100` (not Black's stock 88) pairs well with a Ruff config in the same repo — match both to the same value, or the two tools will disagree on wraps. If the repo also runs Ruff for linting, add `"E501"` to Ruff's ignore list (line length becomes Black's job).

## Installation

```bash
pip install black
# or
pipx install black
```

## More Information
- [Black documentation](https://black.readthedocs.io/)
- [GitHub Repository](https://github.com/psf/black)
