# INOV8Skills

A Claude Code plugin marketplace from INOV8.

This repository is a [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugins) (id: `inov8-plugins`) that bundles INOV8's published plugins. Each plugin ships one or more skills that extend Claude with domain-specific workflows — currently focused on capturing tacit business-process knowledge and querying healthcare price-transparency data.

## Installation

In Claude Code, add the marketplace and install the plugins you want:

```text
/plugin marketplace add recursor/INOV8Skills
/plugin install inov8-process-skills@inov8-plugins
/plugin install transparency-in-coverage-skills@inov8-plugins
/plugin install inov8-exchange-skills@inov8-plugins
/plugin install inov8-credentialing-skills@inov8-plugins
/plugin install inov8-design-skills@inov8-plugins
```

The marketplace can also be added by full git URL or by local filesystem path. The marketplace identifier is `inov8-plugins` (from `.claude-plugin/marketplace.json`), so install commands use the `@inov8-plugins` suffix even though the repo directory is named `INOV8Skills`.

To see what's available without installing:

```text
/plugin marketplace list inov8-plugins
```

### OpenAI Codex

The skills follow the open [Agent Skills](https://learn.chatgpt.com/docs/build-skills) format, so Codex can install them directly from this repo. Inside Codex, run one line per skill, then restart Codex:

```text
$skill-installer install https://github.com/recursor/INOV8Skills/tree/main/plugins/inov8-process-skills/skills/process-interview
$skill-installer install https://github.com/recursor/INOV8Skills/tree/main/plugins/transparency-in-coverage-skills/skills/tic-lookup
$skill-installer install https://github.com/recursor/INOV8Skills/tree/main/plugins/inov8-design-skills/skills/inov8-orthopedics-design
```

Without the installer, copy the skill folder into `~/.agents/skills/`. The `exchange-mcp-setup` skill is Claude Desktop-only and is not useful in Codex.

## Plugins

### `inov8-process-skills`

- **Version:** 0.2.1
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

- **Version:** 0.2.0
- **Category:** healthcare
- **Description:** Skills for indexing and querying CMS Transparency in Coverage (TiC) machine-readable in-network rate files by payer, plan, NPI, and CPT/HCPCS code.

**Skills:**

- **[`tic-lookup`](plugins/transparency-in-coverage-skills/skills/tic-lookup/SKILL.md)** — Downloads pre-filtered payer JSON files (Aetna, BCBS, Cigna, UHC) and an NPPES NPI registry from INOV8's public mirror, builds a SQLite database, and answers payer/plan/NPI/CPT rate questions. Handles indexing, querying, and summarizing only — pair with the `pptx` or `xlsx` skills for reports.

**Example trigger phrases:**

- "what does Aetna pay for a knee replacement"
- "compare facility rates for CPT 27447"
- "look up in-network rates for [payer/plan/NPI]"
- Anything mentioning TiC files, price transparency, or negotiated rates

### `inov8-design-skills`

- **Version:** 0.1.0
- **Category:** design
- **Description:** Skill that fetches the INOV8 Orthopedics design system from the public [`recursor/Design`](https://github.com/recursor/Design) repository and enforces its brand rules, tokens, and component patterns whenever Claude designs or builds INOV8-branded output.

**Skills:**

- **[`inov8-orthopedics-design`](plugins/inov8-design-skills/skills/inov8-orthopedics-design/SKILL.md)** — Clones or fetches `systems/inov8-orthopedics/` from `recursor/Design`, follows that system's own `SKILL.md` (brand book, `tokens.css`, `tokens.json`, component cards and previews), and carries a fallback summary of the hard rules for when the fetch fails. Works in Claude Code and, via `$skill-installer`, in Codex; Codex users can also install the system's own skill straight from the Design repo.

**Example trigger phrases:**

- "make this look like INOV8"
- "INOV8 design system" / "INOV8 colors" / "use our brand"
- "build an INOV8 Orthopedics landing page"

## Microsoft Exchange (Claude Desktop)

Connect Claude Desktop to an on-premises Microsoft Exchange mailbox so chat and cowork can read mail, search the calendar, manage tasks, and look up contacts. Distributed as a Claude Desktop extension (`.mcpb`) — no terminal, no Docker, no Python install required. Claude Desktop manages the runtime; your password is stored in the OS keychain.

### Install

1. Download [`exchange-mcp-server-latest.mcpb`](https://inov8public.z21.web.core.windows.net/ExchangeMCP/exchange-mcp-server-latest.mcpb).
2. In Claude Desktop, open **Settings → Extensions** and drag the `.mcpb` file onto the window.
3. Fill in the form fields and click **Install**. The Exchange tools become available in chat and cowork immediately.

### What you'll need

| Field | Example | Notes |
| --- | --- | --- |
| Account 1 — Exchange server | `mail.contoso.com` | Hostname only — no `https://` |
| Account 1 — Email address | `you@contoso.com` | Your full email |
| Account 1 — Username | `you@contoso.com` | Your email again; plain `jdoe` + a Windows domain only if the server rejects that |
| Account 1 — Windows domain | (blank) | Advanced; usually leave blank |
| Account 1 — Password | — | Stored in the OS keychain |
| Account 1 — Verify SSL | `true` | Set to `false` only for self-signed certs |
| Account 1 — Timezone (IANA) | `America/Chicago` | Defaults to `UTC` |
| Additional mailboxes | `billing@contoso.com` | Shared mailboxes your login can already open, comma-separated |

### Multiple mailboxes

- **Same login, more mailboxes:** list them in **Additional mailboxes**.
- **A second or third login:** fill in the **Account 2 —** and **Account 3 —** fields.
- **Four or more logins:** leave the Account fields blank and set **Multi-account config file** to the absolute path of a `config.json` whose `accounts` array describes each mailbox. See the schema in the [Exchange MCP Server README](https://github.com/recursor/INOV8.MCP/blob/main/ExchangeMCPServer/README.md).

Run the `exchange-mcp-setup` skill (`/plugin install inov8-exchange-skills@inov8-plugins`, then ask Claude to "set up exchange") for a guided walkthrough.

### Source and support

The extension is built from [`recursor/INOV8.MCP`](https://github.com/recursor/INOV8.MCP/tree/main/ExchangeMCPServer) (`ExchangeMCPServer/`). Report issues there.

> **Claude Code users:** Claude Desktop and Claude Code use separate MCP configurations. To use the same Exchange server in Claude Code, register the `uv` invocation in your Claude Code MCP config — see the [Exchange MCP Server README](https://github.com/recursor/INOV8.MCP/blob/main/ExchangeMCPServer/README.md) for the command. The `inov8-exchange-skills` plugin here only covers the Claude Desktop install.

## INOV8 Case Logs (Claude Desktop)

Fetches one physician's case log from INOV8Functions by NPI and renders the credentialing artifacts — an `.xlsx` workbook with **Schedule** and **Operative** tabs, plus one landscape PDF per non-empty tab — on your own machine. Distributed as a Claude Desktop extension (`.mcpb`) — no terminal, no Docker, no Python install required. The underlying rows never flow through the model; only counts and file paths are returned.

### Install

1. Download [`caselog-mcp-server-latest.mcpb`](https://inov8public.z21.web.core.windows.net/CaseLogMCP/caselog-mcp-server-latest.mcpb).
2. In Claude Desktop, open **Settings → Extensions** and drag the `.mcpb` file onto the window.
3. Fill in the three fields below and click **Install**.

### What you'll need

| Field | What to enter | Notes |
| --- | --- | --- |
| Function key | The key provided by INOV8 IT | Sensitive. Stored in the OS keychain. |
| Endpoint base URL | Leave the default | Defaults to `https://inov8functions.azurewebsites.net/api/`. |
| Output folder | Leave the default, or pick a folder | Defaults to `~/Documents/CaseLogs`. |

### Producing a case log

Run the `case-log-mcp-setup` skill (`/plugin install inov8-credentialing-skills@inov8-plugins`, then ask Claude to "set up case logs") for a guided walkthrough, or once installed just ask Claude something like *"run a case log for NPI 1234567890"* (an optional `yyyy-MM-dd`–`yyyy-MM-dd` range; default is three years back through today).

Claude relays the Schedule and Operative row counts and the absolute file paths verbatim — never the rows themselves. A count of `0` means that tab and its PDF were omitted (a non-surgeon with zero Operative rows is expected; a surgeon with zero Operative rows means the NPI should be re-verified).

### Source and support

The extension is built from [`recursor/INOV8.MCP`](https://github.com/recursor/INOV8.MCP/tree/main/CaseLogMCPServer) (`CaseLogMCPServer/`). Report issues there.

> **Claude Code users:** Claude Desktop and Claude Code use separate MCP configurations. To use the same Case Log server in Claude Code, see [Option D of the Case Log MCP Server README](https://github.com/recursor/INOV8.MCP/blob/main/CaseLogMCPServer/README.md#option-d-other-mcp-clients-codex-and-any-stdio-client) for the command. The `inov8-credentialing-skills` plugin here only covers the Claude Desktop install.

## Repository layout

```text
INOV8Skills/
├── .claude-plugin/
│   └── marketplace.json                    # Marketplace manifest (id: inov8-plugins)
├── plugins/
│   ├── inov8-credentialing-skills/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/case-log-mcp-setup/SKILL.md
│   ├── inov8-design-skills/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/inov8-orthopedics-design/SKILL.md
│   ├── inov8-exchange-skills/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/exchange-mcp-setup/SKILL.md
│   ├── inov8-process-skills/
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/process-interview/SKILL.md
│   └── transparency-in-coverage-skills/
│       ├── .claude-plugin/plugin.json
│       └── skills/tic-lookup/SKILL.md
├── docs/
│   ├── agents/                             # Issue-tracker, triage-label, and domain-doc config for engineering skills
│   └── braindump.md                        # Background reading on tacit-knowledge extraction
└── README.md
```

## License

MIT — see each plugin's `plugin.json` for its license declaration.
