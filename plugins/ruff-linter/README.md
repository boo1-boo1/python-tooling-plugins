# ruff-linter

Python linting and code quality checks with Ruff for Claude Code.

## Usage

```
/python-lint [path] [--fix]
```

Or just ask Claude to lint Python code — the skill auto-triggers.

## Lint-on-edit hook

Ships a `PostToolUse` hook (`hooks/hooks.json` → `scripts/lint.py`) that fires after every `Write`/`Edit` on a `.py` file:

- Skips if `ruff` isn't installed, or the project has no `[tool.ruff]` in `pyproject.toml`, no `ruff.toml`/`.ruff.toml`, and no `astral-sh/ruff` entry in `.pre-commit-config.yaml`.
- Runs `ruff check --quiet` on just the edited file (report only — never mutates the file; `--fix` silently strips things like unused imports mid-edit).

Requires `bash` and `python3` (used to parse the hook's JSON input) on `PATH`.

## Recommended configuration

If a project uses Ruff but has no `[tool.ruff]` section yet, the skill offers a baseline (`line-length = 100`, a curated `select` list, `preview = true`) rather than writing it unasked. See the skill's SKILL.md for the exact block.

## Installation

```bash
pip install ruff
# or
pipx install ruff
```

## More Information
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [GitHub Repository](https://github.com/astral-sh/ruff)
