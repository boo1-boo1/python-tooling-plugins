# black-formatter

Python code formatting with Black for Claude Code.

## Usage

```
/python-format [path]
```

Or just ask Claude to format Python code — the skill auto-triggers.

## Format-on-edit hook

Ships a `PostToolUse` hook (`hooks/hooks.json` → `scripts/format-code.py`) that fires after every `Write`/`Edit` on a `.py` file:

- Skips if `black` isn't installed, or the project has no `[tool.black]` in `pyproject.toml` and no `psf/black` entry in `.pre-commit-config.yaml`.
- Runs `black --quiet` on just the edited file.

Requires `bash` and `python3` (used to parse the hook's JSON input) on `PATH`.

## Recommended configuration

If a project uses Black but has no `[tool.black]` section yet, the skill offers a `line-length = 100` baseline rather than writing it unasked — matched to the ruff-linter baseline so the two tools agree on wraps. See the skill's SKILL.md for the exact block.

## Installation

```bash
pip install black
# or
pipx install black
```

## More Information
- [Black documentation](https://black.readthedocs.io/)
- [GitHub Repository](https://github.com/psf/black)
