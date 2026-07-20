# 🧹 purge

An automated message cleanup utility that purges messages in configured channels after a configurable delay, or sweeps older messages periodically.

---

## Features
- **Live Deletion Delay**: Automatically deletes messages in designated channels after a configurable delay (e.g. 1 hour).
- **Maintenance Sweeping**: Hourly background scans to clean up older messages that exceed a specific day limit.
- **Exceptions**: Excludes pinned messages, whitelisted roles, or specific users from deletion.
- **Clean Unloads**: Automatically terminates scheduled deletion tasks on cog unload to prevent memory leaks.

---

## Player Commands
*No player-level command interface registered. Channel cleanup is handled globally or configured by administrators.*

---

## Administrator Commands
Require **Manage Messages** or **Administrator** permissions.

*   **`[p]autoclean toggle`** — Toggles live delayed purging on/off for the current channel.
*   **`[p]autoclean delay <seconds>`** — Sets delay time (in seconds) before deletion.
*   **`[p]autoclean ignoreuser <user>`** — Whitelist a user to bypass message deletion.
*   **`[p]autoclean ignorerole <role>`** — Whitelist a role to bypass message deletion.
*   **`[p]autoclean clearnow <amount>`** — Instantly purges up to 2000 messages in the current channel.
*   **`[p]autoclean status`** — Displays current config status for the channel.
*   **`[p]root`** (or `/root`) — Configure channel toggles, delay settings, and whitelists via the Mainframe dashboard.
