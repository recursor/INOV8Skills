---
name: exchange-setup
description: >
  First-time setup for the INOV8 Exchange MCP plugin. Use when the user invokes
  /exchange-setup, asks "how do I set up the exchange plugin", "configure exchange",
  "set up my exchange credentials", or has installed inov8-exchange-skills and
  has not yet created a config.json. Creates a per-user config file at
  ~/.inov8/exchange-mcp/config.json from the bundled template, then opens it in
  the user's default editor so they can fill in their account details. NEVER
  reads or displays the contents of the populated config file — credentials
  must not enter Claude's conversation context.
---

# Exchange Setup

## What this skill does

Creates the user's Exchange config file (if it doesn't already exist) and opens it in their editor. The user fills in their account credentials (name, server, email, username, domain, password, verify_ssl, timezone) directly in the editor — Claude never sees the values.

## CRITICAL SAFETY RULE

**Do NOT read, cat, head, tail, grep, or otherwise display the contents of the user's `config.json` at any point.** This file contains plaintext Exchange passwords. Reading it would dump the user's credentials into the conversation transcript, which is exactly what this plugin is designed to avoid.

Allowed operations on the user's config.json:
- Check whether it exists (`test -f`, `[ -f ... ]`, `ls`).
- Copy the template TO that path when the file does not yet exist.
- Open the file in an editor (`open`, `xdg-open`, `notepad`, `start`).

Forbidden operations:
- `cat`, `Read`, `head`, `tail`, `less`, `more`, `grep`, `awk`, `sed -n`, `jq` against the user's config.
- Echoing the path's contents in any form.
- Asking the user for credential values to write into the file yourself.

If the user asks you to "show me my config" or "read the file", politely refuse and remind them that this skill is designed to keep their passwords out of the chat. Tell them they can open the file directly in their editor.

## Steps

### 1. Detect platform and resolve config path

The config file lives at:
- macOS / Linux / WSL / Git Bash: `$HOME/.inov8/exchange-mcp/config.json`
- Native Windows: `%USERPROFILE%\.inov8\exchange-mcp\config.json`

Use `uname` to detect platform. On `Darwin` or `Linux`, use `$HOME`. On `MINGW*` / `MSYS*` / `CYGWIN*`, use `$HOME` (Git Bash sets it). If running native PowerShell or cmd, use `$env:USERPROFILE` / `%USERPROFILE%`.

For most Claude Code installs (which run via Git Bash on Windows or natively elsewhere), `$HOME` works.

### 2. Check whether the config already exists

```bash
CONFIG_DIR="$HOME/.inov8/exchange-mcp"
CONFIG_FILE="$CONFIG_DIR/config.json"
if [ -f "$CONFIG_FILE" ]; then
  echo "Config file already exists at $CONFIG_FILE"
  EXISTING=1
else
  EXISTING=0
fi
```

### 3. If it does NOT exist, create the directory and copy the template

```bash
mkdir -p "$CONFIG_DIR"
cp "${CLAUDE_PLUGIN_ROOT}/docker/config.template.json" "$CONFIG_FILE"
chmod 600 "$CONFIG_FILE"
```

`chmod 600` ensures only the user can read the file (no-op on Windows but harmless). On Windows, NTFS inheritance from the user's home directory is generally adequate.

If the file already existed, skip the copy. Do not overwrite — the user may have real credentials in there.

### 4. Open the config file in the user's editor

Choose the command based on platform:

| Platform | Command |
|---|---|
| macOS | `open -t "$CONFIG_FILE"` (opens in TextEdit) — or `open "$CONFIG_FILE"` for the default app |
| Linux | `xdg-open "$CONFIG_FILE"` — fallback: `${EDITOR:-nano} "$CONFIG_FILE"` |
| Windows (Git Bash / WSL) | `notepad "$CONFIG_FILE"` or `start "" "$CONFIG_FILE"` |

Run the command but do not block on it — the editor opens in a separate window. Continue the skill.

### 5. Tell the user what to do next

Print a message like:

> Your Exchange config file is at `<path>` and should be open in your editor.
>
> Fill in these fields for each account:
> - `name` — short label like "work" or "shared-mailbox"
> - `server` — Exchange server hostname (e.g. `mail.inov8hc.com`)
> - `email` — your email address
> - `username` — your Exchange username (often the part before `@`)
> - `domain` — your Active Directory domain
> - `password` — your Exchange password
> - `verify_ssl` — `true` unless your server uses a self-signed cert
> - `timezone` — IANA timezone like `America/Chicago`
>
> Save and close the editor. Then run `/mcp` to confirm the Exchange tools appear. If they don't, restart Claude Code.
>
> To add more accounts later, run `/exchange-add-account`.

If the file already existed, instead say:

> Your Exchange config file already exists at `<path>` and is open in your editor. Add or edit accounts as needed. To add a new account, run `/exchange-add-account` for a blank stanza you can paste in.

## Frontmatter notes for plugin authors

This skill should pre-allow only the specific bash patterns used above. **Do NOT pre-allow `Read` against `~/.inov8/exchange-mcp/config.json` or any glob covering it.** The file's whole purpose is to never enter context.
