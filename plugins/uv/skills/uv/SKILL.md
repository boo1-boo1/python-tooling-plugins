---
name: uv
description: This skill should be used when the user asks to "add a dependency", "install packages", "sync the environment", "lock dependencies", "run a script/command in the venv", or when editing Python files in a project that uses uv for packaging/dependency management.
version: 1.0.0
---

# uv Package/Project Manager

Manages Python dependencies, virtual environments, and project packaging using uv, Astral's fast Rust-based package manager.

## When This Skill Applies

- User asks to add/remove/upgrade a Python dependency, sync or create a venv, lock dependencies, or run something inside the project's environment
- Editing a repo with a `uv.lock` file, a `[tool.uv]` section in `pyproject.toml`, or existing uv usage (CI config, `.python-version` alongside `uv.lock`)
- Never fall back to bare `pip install` in a uv-managed project — it writes into the venv without updating `uv.lock`, silently desyncing the lockfile from what's actually installed.

## Detecting uv Usage

Check for any of:
- `uv.lock` at repo root
- `[tool.uv]` in `pyproject.toml`
- `uv` in `.pre-commit-config.yaml` or CI workflows

If both `uv.lock` and `poetry.lock`/`[tool.poetry]` are present, ask which tool is authoritative before running anything — don't guess.

## No pyproject.toml Found

If uv is invoked (or the user asks to add/install a dependency) in a directory with no `pyproject.toml`, offer to initialize a new project first:

```bash
uv init
```

After init, ask the user whether they also want recommended baseline config added for basedpyright, ruff, and black (see the basedpyright-lsp README and the ruff-linter, black-formatter skills for the exact blocks) — don't write any of it unasked.

## Core Commands

Add a dependency (updates `pyproject.toml` + `uv.lock` + syncs venv):

```bash
uv add requests
uv add --dev pytest        # dev-only dependency group
uv add "django>=5,<6"      # version constraint
```

Remove a dependency:

```bash
uv remove requests
```

Sync the venv to match the lockfile exactly:

```bash
uv sync              # dev workflow, installs all groups
uv sync --frozen      # CI — fail instead of updating the lockfile if it's stale
uv sync --no-dev      # production — skip dev dependency group
```

Regenerate the lockfile without installing:

```bash
uv lock
uv lock --upgrade          # bump all deps to latest allowed versions
uv lock --upgrade-package requests   # bump just one
```

Run a command inside the project's venv (no manual activation needed):

```bash
uv run pytest
uv run python script.py
```

Pin the project's Python version:

```bash
uv python pin 3.12
```

One-off tool execution without adding it as a project dependency:

```bash
uvx ruff check .          # equivalent to: uv tool run ruff check .
```

## Conventions

- uv creates the venv at `.venv/` in the project root by default — don't assume a different location.
- Never hand-edit `uv.lock`; it's fully generated. Change `pyproject.toml` and re-run `uv lock`/`uv sync`.
- `uv add`/`uv remove` already update the lockfile and sync — don't follow them with a separate `uv sync` unless you specifically need `--frozen`/`--no-dev` behavior.
- Respect existing dependency groups (`--dev`, `--group <name>`) already used in `pyproject.toml` rather than dumping everything into main dependencies.

## Installation

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
# or
pipx install uv
```

## More Information
- [uv documentation](https://docs.astral.sh/uv/)
- [GitHub Repository](https://github.com/astral-sh/uv)
