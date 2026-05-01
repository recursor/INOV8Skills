# inov8-exchange-skills

Claude Code plugin that exposes an on-premises Microsoft Exchange server (via Exchange Web Services / EWS) as MCP tools, so Claude Code and Claude Cowork can read, search, send, and manage Exchange email and calendar items on your behalf.

## How it works

- The plugin registers an MCP server in your Claude Code via `.mcp.json`. When the MCP starts, Docker pulls and runs `ghcr.io/recursor/exchangemcpserver:latest` and bind-mounts your config file into the container.
- Your Exchange credentials live in **one file outside the plugin directory**: `~/.inov8/exchange-mcp/config.json`. The plugin never reads this file — only the running container does. Plugin updates won't touch it.
- Two skills handle setup so you never type credentials into Claude:
  - `/exchange-setup` — creates the file from a template and opens it in your editor.
  - `/exchange-add-account` — prints a blank stanza and re-opens the file so you can paste it in.

## Prerequisites

- **Docker.** Required to run the MCP server.
  - macOS: [Docker Desktop](https://www.docker.com/products/docker-desktop/) or [Colima](https://github.com/abiosoft/colima).
  - Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop/).
  - Linux: [Docker Engine](https://docs.docker.com/engine/install/).
- **Network access to your Exchange server.** Your machine must be able to reach the Exchange server (corporate network or VPN).
- **Claude Code** installed locally. Cowork connects through your local Claude Code session's MCP bridge — Code must be running for Cowork to see the Exchange tools.

## Install

From the `inov8-plugins` marketplace:

```text
/plugin marketplace add <git-url-or-local-path-to-INOV8Skills>
/plugin install inov8-exchange-skills@inov8-plugins
```

## First-time setup

```text
/exchange-setup
```

This creates `~/.inov8/exchange-mcp/config.json` from a template and opens it in your default editor. Fill in one account block:

```json
{
  "accounts": [
    {
      "name": "work",
      "server": "mail.inov8hc.com",
      "email": "you@inov8hc.com",
      "username": "you",
      "domain": "inov8hc.com",
      "password": "your-password",
      "verify_ssl": true,
      "timezone": "America/Chicago"
    }
  ]
}
```

Save and close. Then either restart Claude Code or run `/mcp` to reconnect — you should see Exchange tools listed.

## Adding more accounts

```text
/exchange-add-account
```

Prints a blank stanza and re-opens the config file. Paste the stanza into the `accounts` array, fill in real values, save, and restart Claude Code.

## Where credentials live

- File path: `~/.inov8/exchange-mcp/config.json` (macOS/Linux/WSL/Git Bash) or `%USERPROFILE%\.inov8\exchange-mcp\config.json` (Windows).
- File mode: `600` on POSIX (owner read/write only).
- The container mounts this path **read-only**, so the MCP server can't accidentally rewrite credentials.
- The plugin's setup skills are explicitly forbidden from reading this file's contents. Credentials never enter Claude's transcript.

## Verifying the setup

After `/exchange-setup`:

1. Run `/mcp`. You should see `mcp__plugin_inov8-exchange-skills_exchange__*` tools listed.
2. Ask Claude something like *"list the folders in my work mailbox"* or *"show my calendar for tomorrow"*. The MCP tools should be invoked and return real data.

If tools don't appear:
- Check Docker is running: `docker ps`.
- Pull the image manually: `docker pull ghcr.io/recursor/exchangemcpserver:latest`.
- Confirm `~/.inov8/exchange-mcp/config.json` exists and is valid JSON.
- Restart Claude Code.

## Cowork

Cowork uses your local Claude Code session's MCP bridge to access local tools. As long as Claude Code is running locally with this plugin enabled, Cowork sees the Exchange tools too — no separate Cowork setup needed.

## Updating the MCP server

The compose file uses `pull_policy: missing`, so once the image is cached locally, it won't auto-update. To pull a newer version:

```bash
docker pull ghcr.io/recursor/exchangemcpserver:latest
```

Then restart Claude Code.

## Uninstall

```text
/plugin uninstall inov8-exchange-skills@inov8-plugins
```

Your `~/.inov8/exchange-mcp/config.json` is **not removed** — uninstalling the plugin doesn't touch your credentials. Delete it manually if you want a clean slate.

## License

MIT.
