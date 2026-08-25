# pyright-lsp

Python language server (pyright) for Claude Code, providing static type checking and code intelligence.

pyright is Microsoft's static type checker for Python. Use `basedpyright-lsp` instead if the project has adopted basedpyright (stricter defaults); this plugin is the fallback for projects standardized on plain pyright.

## LSP

Registers `pyright-langserver --stdio` as a language server for `.py`/`.pyi` files, giving live type checking/code-intelligence via pyright's built-in LSP.

## Supported Extensions
`.py`, `.pyi`

## Installation

Install pyright globally via npm:

```bash
npm install -g pyright
```

Or with pip:

```bash
pip install pyright
```

Or with pipx (recommended for CLI tools):

```bash
pipx install pyright
```

## More Information
- [pyright documentation](https://microsoft.github.io/pyright/)
- [GitHub Repository](https://github.com/microsoft/pyright)
