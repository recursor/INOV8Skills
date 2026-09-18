---
name: exchange-mcp-setup
description: This skill should be used when an INOV8 user wants to install, set up, or configure the Exchange MCP desktop extension to read their INOV8 email, calendar, tasks, or contacts inside Claude Desktop. Triggers on phrases like "install exchange", "set up exchange MCP", "connect my work email to claude", "read outlook in claude desktop", "configure exchange extension", "add inov8 mailbox to claude", "set up exchange in claude", "install the exchange mcp", "connect my outlook to claude", "read INOV8 email in claude", "add a shared mailbox", "my exchange password changed", or any request to access work email/calendar from Claude. Walks the user through downloading the .mcpb bundle, installing it in Claude Desktop, configuring one login, shared mailboxes, or up to three separate logins against mail.inov8hc.com, verifying it works, and troubleshooting common errors including rejected or locked-out credentials.
version: 0.3.0
---

# Exchange MCP Setup

Walk an INOV8 user through installing the Exchange MCP desktop extension in Claude Desktop and configuring it against `mail.inov8hc.com` so chat and cowork can read their mail, calendar, tasks, and contacts.

## How to use this skill

Relay the steps below to the user in order. Adapt phrasing for chat, but **preserve URLs, field labels, JSON keys, and the example values verbatim** — they are the literal strings the user will see in the install dialog and need to type. Pause after each step and confirm the user is ready to proceed before continuing. If the user reports an error, jump to the Troubleshooting table; do not improvise fixes.

The skill is finished when the user has run the verification prompts in Step 4 and Claude has returned real mailbox data.

## What this is

The Exchange MCP server is a Claude Desktop extension that lets Claude read mail, calendar, tasks, and contacts from INOV8's on-prem Microsoft Exchange server (`mail.inov8hc.com`) over EWS, using NTLM/Windows authentication. Once installed, the user can ask Claude things like *"what meetings do I have today?"* or *"draft a reply to Sarah's last email"*. 19 tools across email, calendar, tasks, contacts, and account management.

**Where the tools show up.** Both Claude Desktop **chat** and **cowork** share the same desktop-extension registry, so installing the `.mcpb` once makes the Exchange tools available in both modes. They do **not** show up in **Claude Code**, even when Claude Code is launched from inside Claude Desktop — Claude Code uses a separate MCP config (`~/.claude.json` / `.mcp.json` / `claude mcp add`). For the Claude Code path, see the [Exchange MCP Server README](https://github.com/recursor/INOV8.MCP/blob/main/ExchangeMCPServer/README.md) for the `uv` invocation to register manually.

## Prerequisites

- **Claude Desktop installed.** Not Claude Code (CLI), not claude.ai, not the web UI. The `.mcpb` format only works in Claude Desktop. Anthropic ships Claude Desktop for **macOS** and **Windows** (incl. ARM64) — see <https://claude.com/download>. Not available on Linux.
- **First-launch internet access (~30 s).** Claude Desktop's bundled `uv` runtime provisions a Python interpreter and the runtime dependencies on first start. No system Python install required.
- **INOV8 credentials.** Email address and Windows password. The email address doubles as the username.

## Step 1 — Download the bundle

The same file is used on macOS and Windows:

<https://inov8public.z21.web.core.windows.net/ExchangeMCP/exchange-mcp-server-latest.mcpb>

## Step 2 — Install via Settings → Extensions

This is the canonical install path documented by Anthropic and works the same on every supported platform:

1. Open **Claude Desktop**.
2. Open **Settings → Extensions**:
   - **macOS:** `⌘,` → click **Extensions** in the sidebar.
   - **Windows:** click the hamburger menu **☰** in the top-left → **File → Settings → Extensions** (or `Ctrl+,`).
3. Expand **Advanced settings** at the bottom of the Extensions page, find the **Extension Developer** section, and click **Install Extension…**, then pick the downloaded `.mcpb`. Drag-and-drop the `.mcpb` from Finder / File Explorer onto the Extensions window also works.
4. Claude Desktop opens the install dialog described in Step 3.

Side-load warnings to expect:

- **macOS:** Gatekeeper may quarantine the file. Right-click the `.mcpb` in Finder → **Open** the first time, or approve via **System Settings → Privacy & Security → Open Anyway**. After it's allowed, double-clicking the `.mcpb` in Finder also opens the install dialog directly.
- **Windows:** SmartScreen may show *"Windows protected your PC"* for an unknown publisher when the bundle is downloaded. Click **More info → Run anyway** on the download, then use the **Settings → Extensions** path above. Double-clicking the `.mcpb` in File Explorer is **not** reliable on Windows — Claude Desktop does not always register the file association — so prefer drag-drop or **Install Extension…**.

## Step 3 — Fill in the install dialog

The dialog has three blocks: **Account 1** (the user's own login), **Additional mailboxes** (shared mailboxes that login can already open), and **Account 2 / Account 3** (mailboxes that need a *different* login). Most users fill Account 1 only.

### Account 1 — the user's own mailbox

| Field (verbatim from the dialog) | What to enter | INOV8 value |
| --- | --- | --- |
| Account 1 — Name | Short name used in prompts. Leave blank to use the part before the `@`. | (blank, or `work`) |
| Account 1 — Exchange server | INOV8's Exchange server | `mail.inov8hc.com` |
| Account 1 — Email address | Your full INOV8 email | `you@inov8hc.com` |
| Account 1 — Username | Your full email address again | `you@inov8hc.com` |
| Account 1 — Windows domain (advanced — usually leave blank) | Leave blank | (blank) |
| Account 1 — Password | Your Windows password (stored in the OS keychain) | `••••••••` |
| Account 1 — Verify SSL | `true` unless the server uses a self-signed cert | `true` |
| Account 1 — Timezone (IANA) | Your IANA timezone (defaults to UTC) | `America/Chicago` |
| Additional mailboxes (comma-separated) | Leave blank unless the user has shared mailboxes (next section) | (blank) |
| Multi-account config file (optional) | Leave blank | (blank) |

Leave every **Account 2 —** and **Account 3 —** field blank. Click **Install**.

If the install later fails with `401 Unauthorized`, the fallback is Windows-style auth: set **Account 1 — Username** to the short Windows username (e.g. `jdoe`) and **Account 1 — Windows domain** to `INOV8HC`. Try the email form first; it works on `mail.inov8hc.com`.

### Shared mailboxes (same login)

If the user's own login already has access to shared or delegated mailboxes (a team inbox, a departmental calendar), no extra credentials are needed. In **Additional mailboxes (comma-separated)** enter their addresses:

```text
billing@inov8hc.com, frontdesk@inov8hc.com
```

Each appears as its own account named after the part before the `@` (`billing`, `frontdesk`), usable in prompts like *"show the billing inbox"*. They use the Account 1 credentials.

### A second or third login (Account 2 / Account 3)

If the user needs a mailbox that requires a *different* username and password, fill the **Account 2 —** block (and **Account 3 —** for a third). Each block has the same fields as Account 1 and is fully independent — nothing is inherited from Account 1, so repeat the server, email, username, password, and timezone. Give each a distinct **Name** (e.g. `personal`, `clinic`).

Four or more separate logins need the config file below.

### Multi-account config file (four or more logins)

Leave all Account fields blank and set **Multi-account config file (optional)** to the absolute path of a JSON file like this:

```json
{
  "accounts": [
    {
      "name": "work",
      "server": "mail.inov8hc.com",
      "email": "you@inov8hc.com",
      "username": "you@inov8hc.com",
      "domain": "",
      "password": "your-password",
      "verify_ssl": true,
      "timezone": "America/Chicago"
    },
    {
      "name": "clinic",
      "server": "mail.inov8hc.com",
      "email": "clinic-user@inov8hc.com",
      "username": "clinic-user@inov8hc.com",
      "domain": "",
      "password": "other-password",
      "verify_ssl": true,
      "timezone": "America/Chicago"
    }
  ]
}
```

Each `name` becomes the account identifier referenced in prompts (*"read my work inbox"*, *"show the clinic calendar"*).

Save the file somewhere private and use an absolute path in the install dialog (no `~`). Suggested locations:

- **macOS:** `/Users/<you>/.exchange-mcp/config.json` — `chmod 600` it.
- **Windows:** `C:\Users\<you>\.exchange-mcp\config.json` — restrict to the user's account.

This file holds plaintext passwords. Treat it like a credential.

## Step 4 — Verify it works

Have the user open a fresh **chat or cowork session** in Claude Desktop and try each:

1. *"Check my Exchange credentials."* — runs one login test per configured account and reports any that were rejected or locked out. Do this first.
2. *"What meetings do I have today?"* — exercises the calendar surface.
3. *"Show me my unread emails."* — exercises the email surface.
4. *"List my tasks."* — exercises the tasks surface.

For shared mailboxes or extra logins, prefix with the account name (*"check the billing inbox"*, *"list my clinic tasks"*). Asking *"list my accounts"* shows what is configured.

If Claude responds with real data, the install is done. If Claude says the tool isn't available, jump to **Troubleshooting**.

## Updating

Claude Desktop does not auto-update side-loaded extensions. To upgrade:

1. Re-download `exchange-mcp-server-latest.mcpb` from the link in Step 1.
2. Re-install via **Settings → Extensions** the same way as Step 2 (drag-drop or **Install Extension…**) and click **Install** in the dialog. Saved credentials carry over (the extension name is stable).

Confirm the version under **Claude Desktop → Settings → Extensions → Microsoft Exchange**.

## Changing a password

After a Windows password change, the extension refuses to retry the old password for that account (and its shared mailboxes) until it is restarted — repeated failed logons can lock the Windows account. Steps:

1. **Claude Desktop → Settings → Extensions → Microsoft Exchange → Configure**, update the password field, save.
2. Quit Claude Desktop fully (`⌘Q` on macOS; right-click the tray icon → **Quit** on Windows) and reopen it.
3. Run *"Check my Exchange credentials."* in a new chat.

## Uninstall

**Claude Desktop → Settings → Extensions → Microsoft Exchange → Remove.** The OS keychain entry is cleared automatically.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `401 Unauthorized` on first install | Re-check the email address and password. Try logging into Outlook Web Access with the same creds — if that fails, the creds are wrong. If OWA works, use the Windows-style fallback from Step 3 (`jdoe` + domain `INOV8HC`). |
| `Credentials rejected for account …` | The password stored in the extension is wrong or has changed. Follow **Changing a password** above. Do not keep retrying. |
| `Account … is locked out by the domain` | Too many failed logons. Wait for the lockout window to expire or contact IT, then follow **Changing a password**. |
| SSL certificate verify failed | Set **Account 1 — Verify SSL** to `false` (string) in the install dialog. |
| `ErrorNonExistentMailbox` | Email address typo, or the mailbox isn't on `mail.inov8hc.com`. For a shared mailbox, confirm the login actually has access to it in Outlook. |
| `Unknown account …` | The name used in the prompt doesn't match a configured account. Ask *"list my accounts"* and use one of those names. |
| Extension not appearing | Quit Claude Desktop fully (⌘Q / right-click tray → Quit) and reopen. First launch needs internet so `uv` can fetch Python (~30 s). |
| First launch hangs > 2 minutes | A strict proxy is likely blocking PyPI / astral.sh. Allowlist `pypi.org`, `files.pythonhosted.org`, and `astral.sh` for the user account. |

If none of these fix it, instruct the user to email **dbalderree@inov8hc.com** with: the error message, their OS, and their Claude Desktop version (**Settings → About**).

## Support

For installation help, bugs, feature requests, or questions: **dbalderree@inov8hc.com**.

## Security

- The password is stored in the OS keychain — Keychain on macOS, Credential Manager on Windows. Never written to disk in plaintext by Claude Desktop.
- The extension only opens stdio (to Claude Desktop) and HTTPS (to `mail.inov8hc.com`). No telemetry, no other outbound traffic.
- The optional multi-account `config.json` **does** store passwords in plaintext. Restrict its permissions and don't commit it.
- After a rejected password the extension stops retrying that account until restarted, so a stale password cannot lock the Windows account.

## What the user can ask Claude to do (tool inventory)

- **Email (8 tools):** list inbox/sent/drafts, search, read full email, send, save draft, reply / reply-all, set categories, delete.
- **Calendar (3):** list calendars (with sub-calendars), list events over a date range, today's meetings.
- **Tasks (4):** list, create, update, complete.
- **Contacts (2):** search, read full details.
- **Accounts (2):** list configured mailboxes, check credentials for every account.
