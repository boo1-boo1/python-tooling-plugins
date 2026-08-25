# Python Tooling Plugins for Claude Code

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Marketplace version](https://img.shields.io/badge/marketplace-v0.2.1-informational.svg)](.claude-plugin/marketplace.json)
[![Plugins](https://img.shields.io/badge/plugins-7-brightgreen.svg)](#plugins)

Claude Code plugins for Python tooling: type checking, formatting, linting, packaging, and testing.

Repo: https://github.com/boo1-boo1/python-tooling-plugins

## Usage

Add this marketplace in Claude Code:

```
/plugin marketplace add boo1-boo1/python-tooling-plugins
```

Then install a plugin:

```
/plugin install basedpyright-lsp
/plugin install pyright-lsp
/plugin install black-formatter
/plugin install ruff-linter
/plugin install uv
/plugin install poetry
/plugin install pytest
```

## Plugins

**Type checking**

| Plugin | Description | Command |
| --- | --- | --- |
| [basedpyright-lsp](plugins/basedpyright-lsp) | Python language server (basedpyright) for type checking and code intelligence (LSP: `basedpyright-langserver`) | — |
| [pyright-lsp](plugins/pyright-lsp) | Python language server (pyright) for type checking and code intelligence (LSP: `pyright-langserver`) | — |

**Formatting & linting**

| Plugin | Description | Command |
| --- | --- | --- |
| [black-formatter](plugins/black-formatter) | Python code formatting with Black, plus a hook that auto-formats on edit | `/python-format [path]` |
| [ruff-linter](plugins/ruff-linter) | Python linting and code quality checks with Ruff, plus a hook that lints on edit | `/python-lint [path] [--fix]` |

**Packaging & dependency management**

| Plugin | Description | Command |
| --- | --- | --- |
| [uv](plugins/uv) | Python packaging/dependency management with uv | `/uv-deps <add\|remove\|sync\|lock\|run> [args]` |
| [poetry](plugins/poetry) | Python packaging/dependency management with Poetry | `/poetry-deps <add\|remove\|install\|lock\|run> [args]` |

**Testing**

| Plugin | Description | Command |
| --- | --- | --- |
| [pytest](plugins/pytest) | Python testing with pytest | `/python-test [path\|-k expr\|-m marker]` |

Commands invoke the plugin's skill explicitly, bypassing auto-detection.
