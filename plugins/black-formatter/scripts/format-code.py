#!/usr/bin/env python3
import json
import os
import re
import shutil
import subprocess
import sys


def is_black_project(project_dir):
    pyproject = os.path.join(project_dir, "pyproject.toml")
    try:
        with open(pyproject) as f:
            if re.search(r"^\[tool\.black\]", f.read(), re.MULTILINE):
                return True
    except OSError:
        pass

    precommit = os.path.join(project_dir, ".pre-commit-config.yaml")
    try:
        with open(precommit) as f:
            if "psf/black" in f.read():
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

    if not shutil.which("black"):
        return

    if not is_black_project(project_dir):
        return

    subprocess.run(["black", "--quiet", file_path], cwd=project_dir)


if __name__ == "__main__":
    main()
