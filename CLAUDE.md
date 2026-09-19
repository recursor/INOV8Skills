# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugins) (id `inov8-plugins`, declared in `.claude-plugin/marketplace.json`) bundling INOV8's published plugins. There is no application code, no build, no test suite — content is markdown skills and JSON manifests, consumed at install time by Claude Code.

The repo directory is named `INOV8Skills`, but install commands use `@inov8-plugins` because that is the marketplace id.

## Layout

```
.claude-plugin/marketplace.json          Marketplace manifest — registers each plugin
plugins/<plugin-name>/
    .claude-plugin/plugin.json           Plugin manifest
    skills/<skill-name>/
        SKILL.md                         Required; YAML frontmatter + imperative body
        references/  assets/  scripts/   Optional, loaded on demand
```

A plugin is "registered" only if it appears in `.claude-plugin/marketplace.json` *and* has its own `plugin.json`. The skill itself is auto-discovered by Claude Code from the plugin's `skills/` directory.

## Versioning rule (must follow)

Three places carry a version for each plugin and they must stay in sync. Whenever a skill's body, frontmatter description, or any plugin-bundled resource is changed materially, bump *all three* together:

1. `plugins/<plugin>/skills/<skill>/SKILL.md` — `version:` in frontmatter
2. `plugins/<plugin>/.claude-plugin/plugin.json` — `"version"`
3. `.claude-plugin/marketplace.json` — the plugin's entry's `"version"`

The top-level `metadata.version` in `marketplace.json` tracks the marketplace as a whole; bump it only when adding/removing plugins or making changes that affect the marketplace shape.

Use semver. Patch (`0.2.0` → `0.2.1`) for typo/clarification fixes; minor (`0.2.0` → `0.3.0`) for new behavior or new trigger phrases; major when breaking the skill's contract (renaming the skill, removing tools/sections users depended on).

A bump is part of the same commit as the content change. Do not split them.

## Adding a new skill or plugin

When creating a new skill, also invoke the `plugin-dev:skill-development` skill — it captures the canonical SKILL.md frontmatter, imperative-form body style, and progressive-disclosure conventions used by the existing skills here.

To add a *new plugin*: create `plugins/<plugin>/.claude-plugin/plugin.json`, add at least one skill under `plugins/<plugin>/skills/`, and register the plugin in `.claude-plugin/marketplace.json`. Mirror the field shape of an existing plugin entry (`name`, `source`, `description`, `version`, `category`, `tags`).

The top-level `README.md` has user-facing install/usage docs for each plugin; update it when the plugin's surface changes (new skill, new triggers, new external dependencies). The README is the authoritative copy for non-technical users — keep it consistent with the SKILL.md.

## Plugins currently in the marketplace

- `inov8-process-skills` — `process-interview` skill: structured SME interview producing SOPs/runbooks, writes to Notion (preferred) or local markdown.
- `transparency-in-coverage-skills` — `tic-lookup` skill: indexes CMS Transparency in Coverage rate files into SQLite and answers payer/plan/NPI/CPT rate questions.
- `inov8-exchange-skills` — `exchange-mcp-setup` skill: walks INOV8 users through installing the Exchange MCP `.mcpb` desktop extension in Claude Desktop. Setup-only — the actual Exchange tools live in `recursor/INOV8.MCP` under `ExchangeMCPServer/` and are surfaced via Claude Desktop's chat and cowork modes (not Claude Code, which uses a separate MCP config).
- `inov8-credentialing-skills` — `case-log-mcp-setup` skill: walks INOV8 users through installing the Case Log MCP `.mcpb` desktop extension in Claude Desktop, then through producing and reading a physician's credentialing case log by NPI. Setup-only — the actual rendering lives in `recursor/INOV8.MCP` under `CaseLogMCPServer/` and is surfaced via Claude Desktop's chat and cowork modes (not Claude Code, which uses a separate MCP config).
- `inov8-design-skills` — `inov8-orthopedics-design` skill: fetches the INOV8 Orthopedics design system from the public `recursor/Design` repo (`systems/inov8-orthopedics/`) and follows that system's own `SKILL.md`; carries a fallback summary of the brand's hard rules.

## Keeping inov8-orthopedics-design in sync with the Design repo

The `inov8-orthopedics-design` skill is a pointer: the design system itself lives in `recursor/Design` under `systems/inov8-orthopedics/`, mirrored from its Claude artifact, with its own `SKILL.md`. This skill's fallback hard-rules list, token names, and file paths mirror that file. When the Design repo's `SKILL.md` or README changes a rule, a token name, or a path named here, update this skill and bump its version.

## Keeping exchange-mcp-setup in sync with the server

The `exchange-mcp-setup` skill mirrors the install dialog and behaviour of the server in `recursor/INOV8.MCP` (`ExchangeMCPServer/manifest.json` drives the dialog labels, `README.md` the troubleshooting). When that server changes anything user-visible — `user_config` titles or fields, the tool inventory, the download URL, prerequisites, or error messages — update the skill's Step 3 table, Step 4 prompts, Troubleshooting table, and tool inventory to match, and bump the version. The server repo's `CLAUDE.md` names this skill as a release-checklist step.

## Keeping case-log-mcp-setup in sync with the server

The `case-log-mcp-setup` skill mirrors the install dialog and behaviour of the server in `recursor/INOV8.MCP` (`CaseLogMCPServer/manifest.json` drives the dialog labels and download URL, `server.py` the tool behavior and error messages). When that server changes anything user-visible — `user_config` titles or fields, the tool inventory, the download URL, prerequisites, or error messages — update the skill's Step 3 table, Step 4/5 prompts, Troubleshooting table, and tool inventory to match, and bump the version.

## Conventions worth knowing

- Skill bodies use **imperative/infinitive form** (verb-first instructions to Claude), and frontmatter `description` uses **third-person** ("This skill should be used when...") with explicit trigger phrases users might type.
- URLs, field labels, JSON keys, and credential examples in install/setup skills are intentionally verbatim — do not paraphrase them when relaying to users.
- When the user asks to commit, default to a single commit that bundles the content change *plus* its version bump(s); do not push without an explicit ask.

## Agent skills

### Issue tracker

Issues live in GitHub Issues for `recursor/INOV8Skills`, driven by the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` plus `docs/adr/` at the repo root, created lazily by `/domain-modeling`. See `docs/agents/domain.md`.
