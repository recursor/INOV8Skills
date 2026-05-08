---
name: exchange-mcp-setup
description: This skill should be used when an INOV8 user wants to install, set up, or configure the Exchange MCP desktop extension to read their INOV8 email, calendar, tasks, or contacts inside Claude Desktop. Triggers on phrases like "install exchange", "set up exchange MCP", "connect my work email to claude", "read outlook in claude desktop", "configure exchange extension", "add inov8 mailbox to claude", "set up exchange in claude", "install the exchange mcp", "connect my outlook to claude", "read INOV8 email in claude", or any request to access work email/calendar from Claude. Walks the user through downloading the .mcpb bundle, installing it in Claude Desktop, configuring single-account or multi-account access against mail.inov8hc.com, verifying it works, and troubleshooting common errors.
version: 0.1.0
---

# Exchange MCP Setup

Walk an INOV8 user through installing the Exchange MCP desktop extension in Claude Desktop and configuring it against `mail.inov8hc.com` so chat and cowork can read their mail, calendar, tasks, and contacts.

## How to use this skill

Relay the steps below to the user in order. Adapt phrasing for chat, but **preserve URLs, field labels, JSON keys, and the example values verbatim** — they are the literal strings the user will see in the install dialog and need to type. Pause after each step and confirm the user is ready to proceed before continuing. If the user reports an error, jump to the Troubleshooting table; do not improvise fixes.

The skill is finished when the user has run the three verification prompts in Step 4 and Claude has returned real mailbox data.

## What this is

The Exchange MCP server is a Claude Desktop extension that lets Claude read mail, calendar, tasks, and contacts from INOV8's on-prem Microsoft Exchange server (`mail.inov8hc.com`) over EWS, using NTLM/Windows authentication. Once installed, the user can ask Claude things like *"what meetings do I have today?"* or *"draft a reply to Sarah's last email"*. 18 tools across email, calendar, tasks, and contacts.

**Where the tools show up.** Both Claude Desktop **chat** and **cowork** share the same desktop-extension registry, so installing the `.mcpb` once makes the Exchange tools available in both modes. They do **not** show up in **Claude Code**, even when Claude Code is launched from inside Claude Desktop — Claude Code uses a separate MCP config (`~/.claude.json` / `.mcp.json` / `claude mcp add`). For the Claude Code path, see the [`ExchangeMCPServer` README](https://github.com/recursor/ExchangeMCPServer#readme) for the `uv` invocation to register manually.

## Prerequisites

- **Claude Desktop installed.** Not Claude Code (CLI), not claude.ai, not the web UI. The `.mcpb` format only works in Claude Desktop. macOS, Windows, and Linux all supported.
- **First-launch internet access (~30 s).** Claude Desktop's bundled `uv` runtime provisions a Python interpreter and the runtime dependencies on first start. No system Python install required.
- **INOV8 credentials.** Email, Windows username, NETBIOS domain, password.

## Step 1 — Download the bundle

One file works on macOS, Windows, and Linux:

<https://inov8public.z21.web.core.windows.net/ExchangeMCP/exchange-mcp-server-latest.mcpb>

## Step 2 — Install via Settings → Extensions

The reliable cross-platform method — and the only method on Windows, where Claude Desktop does **not** register the `.mcpb` file association, so double-clicking does nothing:

1. Open **Claude Desktop**.
2. Go to **Settings → Extensions** (on macOS: `⌘,` → Extensions; on Windows: gear icon → Extensions).
3. If there's an **Advanced settings** section, expand it and click **Install Extension…**, then pick the downloaded `.mcpb`. Otherwise, drag the `.mcpb` file from Finder/Explorer onto the Extensions window.
4. Claude Desktop opens the install dialog described in Step 3.

Side-load warnings to expect:

- **macOS:** Gatekeeper may quarantine the file. Right-click the `.mcpb` in Finder → **Open** the first time, or approve via **System Settings → Privacy & Security → Open Anyway**. Double-clicking the `.mcpb` also works on macOS once allowed.
- **Windows:** SmartScreen may show *"Windows protected your PC"* for an unknown publisher when the bundle is downloaded. Click **More info → Run anyway** on the download, then continue with the drag-drop method above. Double-clicking the file in Explorer is **not** supported.
- **Linux:** No warning expected; use drag-drop.

## Step 3 — Fill in the install dialog

In the dialog Claude Desktop opens, fill the single-account fields **or** use the multi-account escape hatch — not both.

### Single-account install

| Field (verbatim from the dialog) | What to enter | Default / INOV8 value |
| --- | --- | --- |
| Exchange server | INOV8's Exchange server | `mail.inov8hc.com` |
| Email address | Your full INOV8 email | `you@inov8hc.com` |
| Windows username | Windows username, no domain prefix | `jdoe` |
| Windows domain (NETBIOS) | NETBIOS domain name | `INOV8HC.COM` |
| Password | Your Windows password (stored in the OS keychain) | `••••••••` |
| Verify SSL | `true` unless the server uses a self-signed cert | `true` |
| Timezone (IANA) | Your IANA timezone (defaults to UTC) | `America/Chicago` |
| Multi-account config file (optional) | Leave blank | (blank) |

Click **Install**.

### Multi-account install

If the user needs to access more than one mailbox (e.g., their own + a shared mailbox), leave the single-account fields blank and set **Multi-account config file** to the absolute path of a JSON file like this:

```json
{
  "accounts": [
    {
      "name": "work",
      "server": "mail.inov8hc.com",
      "email": "you@inov8hc.com",
      "username": "jdoe",
      "domain": "INOV8HC.COM",
      "password": "your-password",
      "verify_ssl": true,
      "timezone": "America/Chicago"
    },
    {
      "name": "shared",
      "server": "mail.inov8hc.com",
      "email": "shared-mailbox@inov8hc.com",
      "username": "jdoe",
      "domain": "INOV8HC.COM",
      "password": "your-password",
      "verify_ssl": true,
      "timezone": "America/Chicago"
    }
  ]
}
```

Each `name` becomes the account identifier referenced in prompts (*"read my work inbox"*, *"show the shared calendar"*).

Save the file somewhere private and use an absolute path in the install dialog (no `~`). Suggested locations:

- **macOS / Linux:** `/Users/<you>/.exchange-mcp/config.json` — `chmod 600` it.
- **Windows:** `C:\Users\<you>\.exchange-mcp\config.json` — restrict to the user's account.

This file holds plaintext passwords. Treat it like a credential.

## Step 4 — Verify it works

Have the user open a fresh **chat or cowork session** in Claude Desktop and try each:

1. *"What meetings do I have today?"* — exercises the calendar surface.
2. *"Show me my unread emails."* — exercises the email surface.
3. *"List my tasks."* — exercises the tasks surface.

For multi-account installs, prefix with the account name from the config (*"check the shared inbox"*, *"list my work tasks"*). Asking *"list my accounts"* shows what is configured.

If Claude responds with real data, the install is done. If Claude says the tool isn't available, jump to **Troubleshooting**.

## Updating

Claude Desktop does not auto-update side-loaded extensions. To upgrade:

1. Re-download `exchange-mcp-server-latest.mcpb` from the link in Step 1.
2. Re-install via **Settings → Extensions** the same way as Step 2 (drag-drop or **Install Extension…**) and click **Install** in the dialog. Saved credentials carry over (the extension name is stable).

Confirm the version under **Claude Desktop → Settings → Extensions → Microsoft Exchange**.

## Uninstall

**Claude Desktop → Settings → Extensions → Microsoft Exchange → Remove.** The OS keychain entry is cleared automatically.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `401 Unauthorized` | Re-check Windows username, NETBIOS domain (`INOV8HC.COM`), and password. Try logging into Outlook Web Access with the same creds — if that fails, the creds are wrong. |
| SSL certificate verify failed | Set **Verify SSL** to `false` (string) in the install dialog. |
| `ErrorNonExistentMailbox` | Email address typo, or the mailbox isn't on `mail.inov8hc.com`. |
| Extension not appearing | Quit Claude Desktop fully (⌘Q / right-click tray → Quit) and reopen. First launch needs internet so `uv` can fetch Python (~30 s). |
| First launch hangs > 2 minutes | A strict proxy is likely blocking PyPI / astral.sh. Allowlist `pypi.org`, `files.pythonhosted.org`, and `astral.sh` for the user account. |

If none of these fix it, instruct the user to email **dbalderree@inov8hc.com** with: the error message, their OS, and their Claude Desktop version (**Settings → About**).

## Support

For installation help, bugs, feature requests, or questions: **dbalderree@inov8hc.com**.

## Security

- The password is stored in the OS keychain — Keychain on macOS, Credential Manager on Windows, libsecret on Linux. Never written to disk in plaintext by Claude Desktop.
- The extension only opens stdio (to Claude Desktop) and HTTPS (to `mail.inov8hc.com`). No telemetry, no other outbound traffic.
- The optional multi-account `config.json` **does** store passwords in plaintext. Restrict its permissions and don't commit it.

## What the user can ask Claude to do (tool inventory)

- **Email (8 tools):** list inbox/sent/drafts, search, read full email, send, save draft, reply / reply-all, set categories, delete.
- **Calendar (3):** list calendars (with sub-calendars), list events over a date range, today's meetings.
- **Tasks (4):** list, create, update, complete.
- **Contacts (2):** search, read full details.
- **Accounts (1):** list configured mailboxes (multi-account installs).
