# basedpyright-lsp

Python language server (basedpyright) for Claude Code, providing static type checking and code intelligence.

basedpyright is a fork of Pyright with additional features, stricter defaults, and community-driven fixes.

## LSP

Registers `basedpyright-langserver --stdio` as a language server for `.py`/`.pyi` files, giving live type checking/code-intelligence via basedpyright's built-in LSP.

## Supported Extensions
`.py`, `.pyi`

## Recommended Configuration

If basedpyright is used but there's no `[tool.basedpyright]` section in `pyproject.toml` yet, offer (don't auto-apply) this baseline as a starting point — confirm with the user before writing it:

```toml
[tool.basedpyright]
typeCheckingMode = "recommended"
pythonVersion = "3.10" # the repo's minimum supported Python version
```

`recommended` is basedpyright's default `typeCheckingMode` (all rules on, reported as errors or warnings); stating it explicitly documents intent. Match `pythonVersion` to the repo's minimum supported Python — it pairs with the `target-version` in the Ruff/Black configs offered by the ruff-linter/black-formatter skills. Note that adding a `[tool.basedpyright]` section makes the config file authoritative for the environment: discouraged language-server settings are then ignored.

## Installation

Install basedpyright globally via npm:

```bash
npm install -g basedpyright
```

Or with pip:

```bash
pip install basedpyright
```

Or with pipx (recommended for CLI tools):

```bash
pipx install basedpyright
```

## More Information
- [basedpyright on npm](https://www.npmjs.com/package/basedpyright)
- [basedpyright on PyPI](https://pypi.org/project/basedpyright/)
- [GitHub Repository](https://github.com/DetachHead/basedpyright)
