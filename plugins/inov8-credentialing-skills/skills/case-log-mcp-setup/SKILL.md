---
name: case-log-mcp-setup
description: This skill should be used when an INOV8 user wants to install, set up, or configure the Case Log MCP desktop extension to produce a physician's credentialing case log (Schedule and Operative workbook plus PDFs) inside Claude Desktop. Triggers on phrases like "install case logs", "set up case log extension", "run a case log for <surname>", "credentialing case log", "case log for Gualtieri", "why is Operative empty", or any request to produce a physician's schedule or operative log. Walks the user through downloading the .mcpb bundle, installing it in Claude Desktop, filling in the function key/endpoint/output-folder dialog, verifying it works, producing a case log by NPI, reading the counts, and troubleshooting common errors.
version: 0.1.0
---

# Case Log MCP Setup

Walk an INOV8 user through installing the Case Log MCP desktop extension in Claude Desktop, then through producing and reading a physician's credentialing case log.

## How to use this skill

Relay the steps below to the user in order. Adapt phrasing for chat, but **preserve URLs, field titles, and error strings verbatim** — they are the literal strings the user will see in the install dialog and in tool output. Pause after each step and confirm the user is ready to proceed before continuing. If the user reports an error, jump to the Troubleshooting table; do not improvise fixes.

The skill is finished when the user has run the verification prompt in Step 4 and, if they want a case log now, produced one in Step 5.

## What this is

The Case Log MCP server is a Claude Desktop extension that fetches one provider's case log from INOV8Functions by NPI (behind a function key) and renders the credentialing artifacts — a workbook with **Schedule** and **Operative** tabs plus one landscape PDF per non-empty tab — on the user's own machine. It matches the hand-built artifacts Brandi produces today. The underlying rows never flow through the model: the tool fetches, renders to disk, and returns only row counts and file paths. Never open, summarize, or restate the row data yourself, even if you can locate the written files.

## Prerequisites

- **Claude Desktop installed.** Not Claude Code (CLI), not claude.ai, not the web UI. The `.mcpb` format only works in Claude Desktop.
- **A function key from INOV8 IT.** Ask the user's IT contact if they don't already have one.
- **The provider's 10-digit NPI.** There is no roster built into this tool — look it up in INOV8Assist or on the NPPES NPI registry.

## Step 1 — Download the bundle

The same file works on macOS, Windows, and Linux:

<https://inov8public.z21.web.core.windows.net/CaseLogMCP/caselog-mcp-server-latest.mcpb>

## Step 2 — Install via Settings → Extensions

1. Open **Claude Desktop**.
2. Open **Settings → Extensions**:
   - **macOS:** `⌘,` → click **Extensions** in the sidebar.
   - **Windows:** click the hamburger menu **☰** in the top-left → **File → Settings → Extensions** (or `Ctrl+,`).
3. Drag the downloaded `.mcpb` onto the Extensions window, or expand **Advanced settings**, find **Extension Developer**, and click **Install Extension…** to pick the file.
4. Claude Desktop opens the install dialog described in Step 3.

## Step 3 — Fill in the install dialog

Three fields, in this exact order:

| Field (verbatim from the dialog) | What to enter | Notes |
| --- | --- | --- |
| Function key | The key provided by INOV8 IT | Sensitive. Stored in the OS keychain. |
| Endpoint base URL | Leave the default | Defaults to `https://inov8functions.azurewebsites.net/api/`; leave it unless IT says otherwise. |
| Output folder | Leave the default, or pick a folder | Defaults to `~/Documents/CaseLogs`. This is where the workbook and PDFs are written. |

Click **Install**.

## Step 4 — Verify it works

Have the user open a fresh chat or cowork session and ask Claude to check the case-log endpoint (this calls the `check_endpoint` tool). Three outcomes:

- **`OK — key accepted and endpoint reachable`** — install succeeded. Move on to Step 5.
- **`Function key rejected by the endpoint — check the key in Settings → Extensions and restart the extension.`** — the key is wrong or was mistyped. Have the user re-open the extension's settings, re-enter the key, and restart Claude Desktop.
- **`Case-log endpoint unreachable — check your network and the Endpoint base URL.`** or **`Unexpected response from the endpoint (HTTP …).`** — a network or server-side problem; see Troubleshooting.

## Step 5 — Produce a case log

1. Ask the user for the provider's 10-digit NPI, and, optionally, a date range as two dates in `yyyy-MM-dd` format. If they don't give a range, tell them the default is three years back through today.
2. Call `render_case_log` with the NPI (and `from_date`/`to_date` if given).
3. Relay the result **verbatim**: the provider's name, the echoed date range, the Schedule and Operative counts, and every file path returned. Do not reformat, summarize, or add rows of your own.
4. If a count is `0`, its tab and PDF were omitted from the workbook — say so plainly (the tool's own note reads `<name>: 0 rows — tab and PDF omitted`). Explain what a zero means:
   - `isSurgeon: false` with a zero Operative count is expected and normal (a non-surgical provider, e.g. Aldrich).
   - `isSurgeon: true` with a zero Operative count is not expected — tell the user to re-verify the NPI before trusting the result.
   - If both Schedule and Operative are zero, no files were written at all (`No files written: both sources are empty`) — treat this as worth flagging, not routine.
5. Never open, summarize, or restate the rows in the workbook or PDFs — the counts and file paths are the complete answer.

## Updating

Claude Desktop does not auto-update side-loaded extensions. To upgrade:

1. Re-download `caselog-mcp-server-latest.mcpb` from the link in Step 1.
2. Re-install via **Settings → Extensions** the same way as Step 2 and click **Install** in the dialog. The saved function key carries over.

Confirm the version under **Claude Desktop → Settings → Extensions → INOV8 Case Logs**.

## Uninstall

**Claude Desktop → Settings → Extensions → INOV8 Case Logs → Remove.** The OS keychain entry is cleared automatically.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `Function key rejected by the endpoint — check the key in Settings → Extensions and restart the extension.` | The stored key is wrong. Re-enter it in **Settings → Extensions** and restart Claude Desktop. Do not keep retrying the same key. |
| `Unknown provider: no provider with NPI <npi>.` | Double-check the NPI — there is no roster to fuzzy-match against. Confirm it in INOV8Assist or NPPES. |
| `Request rejected by the endpoint: <error>` | The endpoint's own validation message follows the colon verbatim: an invalid NPI, a `from`/`to` date not in `yyyy-MM-dd`, or a `from` after `to`. Fix the input named in the message and retry. |
| `Case-log endpoint unreachable — check your network and the Endpoint base URL.` | Check the user's network connection, then confirm the Endpoint base URL in Settings → Extensions is correct. |
| `Output folder is not writable: <path>.` | Pick a different Output folder in Settings → Extensions, or fix that folder's permissions. |
| Both sources come back with a count of 0 (`No files written: both sources are empty`) | No Schedule or Operative rows exist for that NPI and range. Re-verify the NPI and the date range before assuming the provider truly has no activity. |

If none of these fix it, point the user at Support.

## Support

For installation help, bugs, feature requests, or questions about the underlying server: **dbalderree@inov8hc.com**, or file an issue at <https://github.com/recursor/INOV8.MCP/issues>.

## Security

- The function key is stored in the OS keychain — Keychain on macOS, Credential Manager on Windows — never written to disk in plaintext.
- The key is sent only in the `x-functions-key` request header, never in a URL, log line, or tool return value.
- Row data never leaves the workbook/PDF files written to the Output folder; tool responses carry only counts and file paths, and are never put through the model.

## What the user can ask Claude to do (tool inventory)

- **`render_case_log(npi, from_date, to_date)`** — Fetches one provider's case log by NPI (`from_date`/`to_date` optional, `yyyy-MM-dd`; default range is three years back through today) and renders the Excel workbook and PDF(s), returning counts and file paths only.
- **`check_endpoint()`** — Verifies the configured function key and endpoint base URL are usable. Used during setup (Step 4) and any time the extension seems broken.

## Keeping this skill in sync with the server

This skill mirrors the install dialog and behavior of the server in `recursor/INOV8.MCP` (`CaseLogMCPServer/manifest.json` drives the dialog fields and download URL, `server.py` the tool behavior and every error string above) the same way `exchange-mcp-setup` tracks `ExchangeMCPServer/`. When that server changes anything user-visible — `user_config` titles or fields, the tool inventory, the download URL, prerequisites, or error messages — update this skill's Step 3 table, Step 4/5 prompts, Troubleshooting table, and Tool inventory to match, and bump the version.
