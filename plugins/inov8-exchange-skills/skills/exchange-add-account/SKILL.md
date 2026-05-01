---
name: exchange-add-account
description: >
  Add a new account stanza to the INOV8 Exchange MCP config file. Use when the
  user invokes /exchange-add-account, says "add another exchange account", "add
  a shared mailbox", or wants to configure an additional account on top of their
  existing setup. Prints a blank account stanza for the user to paste, then
  opens ~/.inov8/exchange-mcp/config.json in their editor. NEVER reads the
  existing contents of the config file — credentials must not enter Claude's
  conversation context.
---

# Add an Exchange Account

## What this skill does

Prints a blank account stanza and opens the user's existing Exchange config file in their editor. The user pastes the stanza into the `accounts` array and fills it in directly. Claude never sees the file's contents.

## CRITICAL SAFETY RULE

**Do NOT read, cat, head, tail, grep, or otherwise display the contents of the user's `config.json` at any point.** It contains plaintext passwords for accounts they've already configured.

Allowed: check existence, open in editor.
Forbidden: read, parse, modify, or display the file's contents in any form.

## Steps

### 1. Verify the config file exists

```bash
CONFIG_FILE="$HOME/.inov8/exchange-mcp/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
  echo "No Exchange config found at $CONFIG_FILE."
  echo "Run /exchange-setup first to create the initial config."
  exit 0
fi
```

If missing, point the user to `/exchange-setup` and stop. Do not create the file in this skill — that's the setup skill's job, and it has the template.

### 2. Print a blank account stanza for the user to copy

Print this exactly, in a fenced code block, with a clear header:

> Copy this block and paste it as a new entry inside the `accounts` array in your config. Fill in your real values, then save the file.

```json
{
  "name": "shared-mailbox",
  "server": "mail.example.com",
  "email": "shared@example.com",
  "username": "shared",
  "domain": "example.com",
  "password": "REPLACE-WITH-YOUR-PASSWORD",
  "verify_ssl": true,
  "timezone": "America/Chicago"
}
```

Remind the user that JSON requires a comma between array items, so the existing last account needs a trailing comma after its closing brace before the new entry.

### 3. Open the config file in the user's editor

Same per-platform command as `/exchange-setup`:

| Platform | Command |
|---|---|
| macOS | `open -t "$CONFIG_FILE"` |
| Linux | `xdg-open "$CONFIG_FILE"` (fallback `${EDITOR:-nano} "$CONFIG_FILE"`) |
| Windows | `notepad "$CONFIG_FILE"` |

### 4. Tell the user what to do next

> Your config file is open in your editor. Paste the new account block into the `accounts` array, fill in your real values, and save. Then restart Claude Code (or run `/mcp` to reconnect) so the new account is picked up.
