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

## Microsoft Exchange (Claude Desktop)

Connect Claude Desktop to an on-premises Microsoft Exchange mailbox so chat and cowork can read mail, search the calendar, manage tasks, and look up contacts. Distributed as a Claude Desktop extension (`.mcpb`) — no terminal, no Docker, no Python install required. Claude Desktop manages the runtime; your password is stored in the OS keychain.

### Install

1. Download [`exchange-mcp-server-latest.mcpb`](https://inov8public.z21.web.core.windows.net/ExchangeMCP/exchange-mcp-server-latest.mcpb).
2. In Claude Desktop, open **Settings → Extensions** and drag the `.mcpb` file onto the window.
3. Fill in the form fields and click **Install**. The Exchange tools become available in chat and cowork immediately.

### What you'll need

| Field | Example | Notes |
| --- | --- | --- |
| Exchange server | `mail.contoso.com` | Hostname only — no `https://` |
| Email address | `you@contoso.com` | Your full email |
| Windows username | `jdoe` | Without the domain prefix |
| Windows domain (NETBIOS) | `CONTOSO` | The short AD/NETBIOS name |
| Password | — | Stored in the OS keychain |
| Verify SSL | `true` | Set to `false` only for self-signed certs |
| Timezone (IANA) | `America/Chicago` | Defaults to `UTC` |

### Multiple mailboxes

Leave the single-account fields blank and set **Multi-account config file** to the absolute path of a `config.json` whose `accounts` array describes each mailbox. See the schema in the [`ExchangeMCPServer` README](https://github.com/recursor/ExchangeMCPServer#readme).

### Source and support

The extension is built from [`recursor/ExchangeMCPServer`](https://github.com/recursor/ExchangeMCPServer). Report issues there.

> **Claude Code users:** Claude Desktop and Claude Code use separate MCP configurations. To use the same Exchange server in Claude Code, register the `uv` invocation in your Claude Code MCP config — see the [`ExchangeMCPServer` README](https://github.com/recursor/ExchangeMCPServer#readme) for the command. There is no Exchange plugin in this marketplace.

## Repository layout

```text
INOV8Skills/
├── .claude-plugin/
│   └── marketplace.json                    # Marketplace manifest (id: inov8-plugins)
├── plugins/
│   ├── inov8-process-skills/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/process-interview/SKILL.md
│   └── transparency-in-coverage-skills/
│       ├── .claude-plugin/plugin.json
│       └── skills/tic-lookup/SKILL.md
├── docs/
│   └── braindump.md                        # Background reading on tacit-knowledge extraction
└── README.md
```

## License

MIT — see each plugin's `plugin.json` for its license declaration.
