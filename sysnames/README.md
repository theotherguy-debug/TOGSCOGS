# 🏷️ sysnames

A Red-DiscordBot utility that formats server members' nicknames into terminal-themed and script-themed strings (e.g. file paths, prompt inputs, code files) using mathematical monospace characters for a premium matrix look.

## Features
- **Monospace Font Conversion**: Converts standard alphanumeric characters (`A-Z`, `a-z`, `0-9`) into mathematical monospace equivalents to preserve the look and feel of a system terminal.
- **Themed Styling Options**:
  - `terminal`: Command prompts and file extensions (e.g. `C:\Users\username`, `username.py`, `root@username:~$`).
  - `virus`: Known malware and system infections (e.g. `Trojan.Win32.username`, `WannaCry.username`, `Stuxnet.username`).
  - `database`: SQL and Key-Value structures (e.g. `SELECT * FROM username`, `db.users.find(username)`).
  - `network`: IP addresses and networking protocols (e.g. `127.0.0.1/username`, `https://username`).
  - `system`: System kernel directories and drivers (e.g. `dev/sda1/username`, `username.sys`).
  - `all`: Dynamically blends all themes together, selecting randomly.
- **Join Automation**: When enabled, automatically formats new members when they join.
- **Length Safety**: Automatically truncates names so they never exceed Discord's 32-character limit.

## Commands
*   `[p]terminalnames toggle` — Toggles auto-formatting on join.
*   `[p]terminalnames theme <theme>` — Sets active theme (`all`, `terminal`, `virus`, `database`, `network`, `system`).
*   `[p]terminalnames formatall` — Formats all server members.
*   `[p]terminalnames formatmember <member>` — Formats a specific member.
*   `[p]terminalnames resetall` — Clears all custom formatting.
*   `[p]terminalnames status` — Shows active configuration.
