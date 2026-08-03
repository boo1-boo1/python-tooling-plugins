# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A Claude Code **plugin marketplace** — no application code, no build/test/lint tooling of its own. It's a static collection of plugin manifests and skill definitions consumed by Claude Code's `/plugin marketplace add` mechanism.

## Structure

```
.claude-plugin/
  marketplace.json     # marketplace manifest — lists every plugin, single source of truth for what's installable
plugins/
  <plugin-name>/
    .claude-plugin/
      plugin.json       # plugin manifest (name, description, version, author) — omitted for LSP-only plugins
    skills/
      <skill-name>/
        SKILL.md        # model-invoked skill definition (frontmatter: name, description, version)
    commands/
      <name>.md          # slash command (frontmatter: description, argument-hint) that invokes the skill for explicit/manual triggering
    hooks/
      hooks.json          # lifecycle hook config (optional, only on plugins that ship one)
    scripts/              # scripts hooks.json invokes, referenced via ${CLAUDE_PLUGIN_ROOT} (sibling of hooks/, not nested)
    README.md
    LICENSE
```

All current plugins (`basedpyright-lsp`, `pyright-lsp`, `black-formatter`, `ruff-linter`, `uv`, `poetry`, `pytest`) are **skill-based**: each ships a `plugin.json` + `skills/<name>/SKILL.md` + `commands/<name>.md`. The skill triggers when Claude detects relevant Python tooling config (e.g. `[tool.black]`/`[tool.ruff]`/`[tool.basedpyright]`/`[tool.pyright]`/`[tool.uv]`/`[tool.poetry]`/pytest config in `pyproject.toml`) or the user asks directly. `basedpyright-lsp` and `pyright-lsp` additionally keep an `lspServers` block inline in `marketplace.json` (no `plugin.json` needed for that block alone).

A plugin can also be **LSP-only**: no `plugin.json`, just an `lspServers` block in `marketplace.json` mapping file extensions to a language server command. It becomes hybrid the moment it needs a non-LSP command (e.g. a CLI-driven `/python-typecheck`, as `basedpyright-lsp` and `pyright-lsp` did): add `plugin.json` + skill + command to it same as skill-based plugins, keep the `lspServers` block in marketplace.json unchanged. Also add `"strict": false` to that plugin's marketplace entry — once it has both plugin.json-declared components (skill/command) and marketplace-entry-declared components (`lspServers`), Claude Code treats that as conflicting manifests and errors without it.

`lspServers.args` isn't uniform — check the binary's own docs before assuming stdio is default (e.g. `basedpyright-langserver`/`pyright-langserver` need explicit `--stdio`).

A plugin can also ship a **hook** (`hooks/hooks.json` in plugin root + optional `scripts/` it invokes) for automated behavior on lifecycle events (e.g. a `PostToolUse` hook auto-running a check after edits). Reference `${CLAUDE_PLUGIN_ROOT}` for script paths, `${CLAUDE_PROJECT_DIR}` for project-local paths. See [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference.md) for the full hook schema.

Plugins are grouped by function in `marketplace.json` and the README table: type checking → formatting/linting → packaging/dependency management → testing. Keep new plugins slotted into the matching group rather than appended at the end.

A skill for a formatter/linter/type-checker can include a "Recommended Configuration" section: a baseline config block to *offer* (never auto-write) when the tool is used but has no config yet in `pyproject.toml`. Confirm with the user before writing it. See `ruff-linter`, `black-formatter`, `basedpyright-lsp` SKILL.md for the pattern.

A skill for a packaging/dependency manager (`uv`, `poetry`) can include a "No pyproject.toml Found" section: if invoked with no `pyproject.toml` present, offer to init a new project (`uv init`/`poetry init`) first, then ask whether to also add the recommended config from the formatter/linter/type-checker skills above. Confirm before writing anything. See `uv`, `poetry` SKILL.md for the pattern.

## Adding or editing a plugin

1. Add/edit the plugin's entry in `.claude-plugin/marketplace.json` (`plugins` array) — this is what makes it installable and is the authoritative list.
2. For skill-based plugins: create `plugins/<name>/.claude-plugin/plugin.json` and `plugins/<name>/skills/<name>/SKILL.md`. SKILL.md frontmatter description should name the exact trigger phrases (see existing skills for the pattern: "when user asks to X", "when editing Y files in a project that uses Z").
   Also add `plugins/<name>/commands/<name>.md` — a slash command (frontmatter: `description`, `argument-hint`) whose body tells Claude to invoke the skill, so users can trigger explicitly instead of relying on auto-detection.
3. For LSP-only plugins: skip `plugin.json`; add the `lspServers` block directly under the plugin's marketplace.json entry.
   If a plugin later goes hybrid (gains a skill/command alongside its `lspServers` block), also set `"strict": false` on its marketplace entry — see Structure section above.
4. Update the plugin table in root `README.md`. Also add the `/plugin install <name>` line to the Usage section's install list.
5. Keep `version` fields in sync between `plugin.json` and the marketplace entry.
6. Add `LICENSE` and `README.md` to the new plugin dir (see existing plugins for pattern).

No CI, no package manager, no build step — validate by checking JSON is well-formed and SKILL.md frontmatter matches the pattern of existing skills.

Don't trust a subagent's report of hooks/lspServers/mcpServers schema fields at face value — cross-check against the actual [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference.md) before committing. A wrong field name fails silently (the feature just never fires), and this repo has no CI to catch it.

```bash
jq empty .claude-plugin/marketplace.json plugins/*/.claude-plugin/plugin.json plugins/*/hooks/hooks.json
```

## Versioning

Two independent SemVer counters. Don't conflate them.

**Per-plugin version** — lives in each `plugins/<name>/.claude-plugin/plugin.json` AND the matching marketplace `plugins[]` entry. Keep the two in sync. Bump when *that plugin's* internals change:
- `major` — remove a capability or otherwise break consumers (e.g. dropping an `lspServers` block a user relied on).
- `minor` — add a feature (new command, new skill trigger, added LSP).
- `patch` — fix or docs-only change inside the plugin.

**Marketplace version** — `metadata.version` in `marketplace.json`. Tracks the *catalog*, not any single plugin. Bump when:
- `major` — remove or rename a plugin, or break the marketplace schema/structure (consumers resolve differently).
- `minor` — add a plugin to the `plugins` array.
- `patch` — catalog metadata fixups (owner, description).

A plugin-internal change bumps only that plugin's version, never the marketplace. Catalog membership or shape changing bumps only the marketplace version.

Reordering the `plugins` array (e.g. grouping by function) needs no bump — plugins resolve by name, not position, so it's purely cosmetic.

Git tags: cosmetic only — Claude Code consumes the marketplace via `/plugin marketplace add` reading HEAD, not tags. Version fields remain the source of truth. Tag each marketplace `metadata.version` bump as `v<version>` (e.g. `v0.2.1`) on the commit that introduces it, for human/browsing reference.

On each marketplace version tag, also cut a GitHub Release (`gh release create v<version>`) summarizing the commits since the previous tag — purely for discoverability (Releases tab), not consumed by Claude Code.

README carries badges for license, marketplace version, and plugin count at the top — bump the version badge and plugin-count badge alongside any marketplace version/plugin-count change.
