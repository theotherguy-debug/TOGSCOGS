# 🏷️ sysnames

A Redbot utility that formats server members' nicknames into terminal-themed and script-themed strings (e.g. file paths, prompt inputs, code files) using mathematical monospace characters for a premium matrix look.

---

## Features
- **Monospace Font Conversion**: Converts standard alphanumeric characters (`A-Z`, `a-z`, `0-9`) into mathematical monospace equivalents to preserve the look of a system terminal.
- **Themed Styling Options**:
  - `terminal`: Command prompts and file extensions (e.g. `C:\Users\username`, `username.py`, `root@username:~$`).
  - `virus`: Known malware and system infections (e.g. `Trojan.Win32.username`, `WannaCry.username`, `Stuxnet.username`).
  - `database`: SQL and Key-Value structures (e.g. `SELECT * FROM username`, `db.users.find(username)`).
  - `network`: IP addresses and networking protocols (e.g. `127.0.0.1/username`, `https://username`).
  - `system`: System kernel directories and drivers (e.g. `dev/sda1/username`, `username.sys`).
  - `all`: Dynamically blends all themes together, selecting randomly.
- **Join Automation**: Automatically formats new members when they join (if enabled).
- **Length Safety**: Automatically truncates names so they never exceed Discord's 32-character limit.

---

## Player Commands
*No player-level command interface registered. Formatting is handled automatically on join or applied by administrators.*

---

## Administrator Commands
Require **Manage Nicknames** or **Administrator** permissions.

*   **`[p]terminalnames toggle`** — Toggles join auto-formatting.
*   **`[p]terminalnames theme <theme>`** — Sets active theme (`all`, `terminal`, `virus`, `database`, `network`, `system`).
*   **`[p]terminalnames formatall`** — Formats all server members' nicknames.
*   **`[p]terminalnames formatmember <member>`** — Formats a specific member's nickname.
*   **`[p]terminalnames resetall`** — Clears all formatting, reverting nicknames back to default.
*   **`[p]terminalnames status`** — Displays current configuration settings.
*   **`[p]root`** (or `/root`) — Access nickname configuration settings through the interactive mainframe panel.
