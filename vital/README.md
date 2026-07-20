# 🏥 vital

A utility that sends cheekily hostile, terminal-themed well-being reminders to designated channels at randomized intervals. The alerts automatically delete after a specified period to keep channels clean.

---

## Features
- **Variable Broadcast Loop**: Alerts are sent on a random timer (e.g. every 3 to 6 hours) to prevent predictable spam.
- **Terminal Aesthetics**: Reminders are formatted with simulated "System Compromise" ASCII boxes warning about dehydration, poor posture, screen staring, or lack of hygiene.
- **Self-Deleting Warnings**: Dispatched alerts automatically delete themselves after 24 hours.
- **Configurable Alerts**: Combines built-in messages, external `alerts.json` lists, and custom server-specific alerts.

---

## Player Commands
*No player-level command interface registered. Wellbeing loops are managed globally by administrators.*

---

## Administrator Commands
Require **Manage Guild** or **Administrator** permissions.

*   **`[p]system addchannel`** — Adds the current channel to wellbeing alert broadcasts.
*   **`[p]system removechannel`** — Removes the current channel from broadcasts.
*   **`[p]system interval <min_hours> <max_hours>`** — Sets random broadcast timer boundaries.
*   **`[p]system addalert <text>`** — Appends a custom text alert.
*   **`[p]system test`** — Instantly triggers a test reminder in the channel (self-deletes in 5 minutes).
*   **`[p]root`** (or `/root`) — Configure wellbeing channels and broadcast intervals via the Mainframe dashboard.
