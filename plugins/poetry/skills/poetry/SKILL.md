---
name: poetry
description: This skill should be used when the user asks to "add a dependency", "install packages", "lock dependencies", "run a script/command in the venv", "build/publish the package", or when editing Python files in a project that uses Poetry for packaging/dependency management.
version: 1.0.0
---

# Poetry Package/Project Manager

Manages Python dependencies, virtual environments, and packaging/publishing using Poetry.

## When This Skill Applies

- User asks to add/remove/upgrade a Python dependency, install the environment, lock dependencies, run something inside the project's environment, or build/publish the package
- Editing a repo with a `poetry.lock` file, a `[tool.poetry]` section in `pyproject.toml`, or existing Poetry usage (CI config, pre-commit config)
- Never fall back to bare `pip install` in a Poetry-managed project — it writes into the venv without updating `poetry.lock`, silently desyncing the lockfile from what's actually installed.

## Detecting Poetry Usage

Check for any of:
- `poetry.lock` at repo root
- `[tool.poetry]` in `pyproject.toml`
- `poetry` in `.pre-commit-config.yaml` or CI workflows

If both `poetry.lock` and `uv.lock`/`[tool.uv]` are present, ask which tool is authoritative before running anything — don't guess.

## No pyproject.toml Found

If Poetry is invoked (or the user asks to add/install a dependency) in a directory with no `pyproject.toml`, offer to initialize a new project first:

```bash
poetry init
```

After init, ask the user whether they also want recommended baseline config added for basedpyright, ruff, and black (see the basedpyright-lsp README and the ruff-linter, black-formatter skills for the exact blocks) — don't write any of it unasked.

## Core Commands

Add a dependency (updates `pyproject.toml` + `poetry.lock` + installs it):

```bash
poetry add requests
poetry add --group dev pytest      # dev-only dependency group
poetry add "django>=5,<6"          # version constraint
```

Remove a dependency:

```bash
poetry remove requests
```

Install the environment to match the lockfile:

```bash
poetry install                     # dev workflow, installs all groups
poetry install --sync              # also remove packages no longer in the lockfile
poetry install --without dev       # skip a dependency group
poetry install --no-root           # skip installing the project package itself
```

Regenerate the lockfile without installing:

```bash
poetry lock
```

Run a command inside the project's venv:

```bash
poetry run pytest
poetry run python script.py
```

Spawn a shell inside the venv:

```bash
poetry shell
```

Show environment info (venv path, Python version):

```bash
poetry env info
```

Build/publish the package:

```bash
poetry build
poetry publish
```

## Conventions

- Poetry manages venvs outside the project by default (under its cache dir), unless `virtualenvs.in-project = true` is set in config — check `poetry config --list` or `poetry env info` before assuming `.venv/` exists locally.
- Never hand-edit `poetry.lock`; it's fully generated. Change `pyproject.toml` and re-run `poetry lock`/`poetry install`.
- `poetry add`/`poetry remove` already update the lockfile and install — don't follow them with a separate `poetry install` unless you specifically need `--sync`/`--without` behavior.
- Respect existing dependency groups (`--group <name>`) already used in `pyproject.toml` rather than dumping everything into main dependencies.

## Installation

```bash
curl -sSL https://install.python-poetry.org | python3 -
# or
pipx install poetry
```

## More Information
- [Poetry documentation](https://python-poetry.org/docs/)
- [GitHub Repository](https://github.com/python-poetry/poetry)
