#!/usr/bin/env python3
import json
import os
import re
import shutil
import subprocess
import sys


def is_ruff_project(project_dir):
    pyproject = os.path.join(project_dir, "pyproject.toml")
    try:
        with open(pyproject) as f:
            if re.search(r"^\[tool\.ruff\]", f.read(), re.MULTILINE):
                return True
    except OSError:
        pass

    if os.path.isfile(os.path.join(project_dir, "ruff.toml")) or os.path.isfile(
        os.path.join(project_dir, ".ruff.toml")
    ):
        return True

    precommit = os.path.join(project_dir, ".pre-commit-config.yaml")
    try:
        with open(precommit) as f:
            if "astral-sh/ruff" in f.read():
                return True
    except OSError:
        pass

    return False


def main():
    hook_input = json.load(sys.stdin)
    file_path = hook_input.get("tool_input", {}).get("file_path", "")

    if not file_path.endswith(".py") or not os.path.isfile(file_path):
        return

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")

    if not shutil.which("ruff"):
        return

    if not is_ruff_project(project_dir):
        return

    subprocess.run(["ruff", "check", "--quiet", file_path], cwd=project_dir)


if __name__ == "__main__":
    main()
