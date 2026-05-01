# INOV8Skills

A Claude Code plugin marketplace from INOV8.

This repository is a [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugins) (id: `inov8-plugins`) that bundles INOV8's published plugins. Each plugin ships one or more skills that extend Claude with domain-specific workflows — currently focused on capturing tacit business-process knowledge and querying healthcare price-transparency data.

## Installation

In Claude Code, add the marketplace and install the plugins you want:

```text
/plugin marketplace add <git-url-or-local-path-to-this-repo>
/plugin install inov8-process-skills@inov8-plugins
/plugin install transparency-in-coverage-skills@inov8-plugins
```

The marketplace can be added by git URL or by local filesystem path. The marketplace identifier is `inov8-plugins` (from `.claude-plugin/marketplace.json`), so install commands use the `@inov8-plugins` suffix even though the repo directory is named `INOV8Skills`.

To see what's available without installing:

```text
/plugin marketplace list inov8-plugins
```

## Plugins

### `inov8-process-skills`

- **Version:** 0.1.0
- **Category:** knowledge-management
- **Description:** Skills for capturing and structuring business process knowledge from subject-matter experts. Turns Claude into a disciplined process knowledge-engineer that runs structured, multi-phase interviews and produces documentation artifacts.

**Skills:**

- **[`process-interview`](plugins/inov8-process-skills/skills/process-interview/SKILL.md)** — Conducts a structured interview using contextual inquiry, ACTA Knowledge-Audit probes, the Critical Decision Method, and the Critical Incident Technique to extract tacit process knowledge from an SME. Output formats include SOP, runbook, training module, decision flowchart, mistake-prevention checklist, and Cognitive Demands Table. Writes to Notion when available, with local markdown as fallback.

**Example trigger phrases:**

- "interview me about my process"
- "brain dump my workflow"
- "extract my process" / "document this process" / "capture this SOP"
- `/process-interview`

### `transparency-in-coverage-skills`

- **Version:** 0.1.0
- **Category:** healthcare
- **Description:** Skills for indexing and querying CMS Transparency in Coverage (TiC) machine-readable in-network rate files by payer, plan, NPI, and CPT/HCPCS code.

**Skills:**

- **[`tic-lookup`](plugins/transparency-in-coverage-skills/skills/tic-lookup/SKILL.md)** — Downloads pre-filtered payer JSON files (Aetna, BCBS, Cigna, UHC) and an NPPES NPI registry from INOV8's public mirror, builds a SQLite database, and answers payer/plan/NPI/CPT rate questions. Handles indexing, querying, and summarizing only — pair with the `pptx` or `xlsx` skills for reports.

**Example trigger phrases:**

- "what does Aetna pay for a knee replacement"
- "compare facility rates for CPT 27447"
- "look up in-network rates for [payer/plan/NPI]"
- Anything mentioning TiC files, price transparency, or negotiated rates

### `inov8-exchange-skills`

- **Version:** 0.1.0
- **Category:** productivity
- **Description:** MCP server and skills for interacting with on-premises Microsoft Exchange accounts via Exchange Web Services (EWS). Bundles a Docker-based MCP server (`ghcr.io/recursor/exchangemcpserver`) and setup skills that keep credentials in a per-user config file outside the plugin directory.

**Skills:**

- **[`exchange-setup`](plugins/inov8-exchange-skills/skills/exchange-setup/SKILL.md)** — Creates `~/.inov8/exchange-mcp/config.json` from a bundled template and opens it in the user's editor. Designed so credentials never enter Claude's conversation context.
- **[`exchange-add-account`](plugins/inov8-exchange-skills/skills/exchange-add-account/SKILL.md)** — Prints a blank account stanza and re-opens the config for the user to paste in.

**Example trigger phrases:**

- `/exchange-setup`
- "set up exchange" / "configure my exchange account"
- `/exchange-add-account`
- "add another exchange mailbox"

**Prerequisites:** Docker (Desktop, Colima, or Engine) and network access to your Exchange server. See the [plugin README](plugins/inov8-exchange-skills/README.md) for full setup instructions.

## Repository layout

```text
INOV8Skills/
├── .claude-plugin/
│   └── marketplace.json                    # Marketplace manifest (id: inov8-plugins)
├── plugins/
│   ├── inov8-process-skills/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/process-interview/SKILL.md
│   ├── transparency-in-coverage-skills/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/tic-lookup/SKILL.md
│   └── inov8-exchange-skills/
│       ├── .claude-plugin/plugin.json
│       ├── .mcp.json                    # Registers the Exchange MCP server
│       ├── docker/                      # Compose file + config template
│       └── skills/
│           ├── exchange-setup/SKILL.md
│           └── exchange-add-account/SKILL.md
├── docs/
│   └── braindump.md                        # Background reading on tacit-knowledge extraction
└── README.md
```

## License

MIT — see each plugin's `plugin.json` for its license declaration.
