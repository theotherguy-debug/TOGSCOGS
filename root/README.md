# ⚙️ root

The central administrative Mainframe Command Center for your gaming cogs. It offers a fully button-based, modal-driven configuration dashboard for managing your server.

## Features
- **Central Control**: Manage counting, nicknames, hacking settings, auto-cleanup, wellbeing alerts, and server bank accounts from one panel.
- **Button & Select Controls**: No commands needed. Click buttons to trigger tasks, select options from dropdown menus, and fill out pop-up text forms (Modals).
- **🚨 Broadcast DM Subsystem**: 
  - Send direct message broadcasts to specific role groups or everyone in the server (`all`).
  - Spawns a background delivery process with a **1.5-second cooldown delay** between each user to prevent Discord rate-limiting.
  - Automatically skips closed DMs and sends a completion summary DM to the administering operator when finished.
- **Subsystem Integrations**:
  - **Counting**: Toggle channels, enable Survivor Rules, set current counts, grant save tokens, adjust save token prices, set prestige count targets, configure entry license fees, and set global nickname shaming tags and lockout times.
  - **Nicknames**: Set Monospace themes server-wide, toggle auto-format on member join, format specific users by ID, or bulk-reset all member nicknames.
  - **Hacking**: Toggle firewall lockdowns.
  - **AutoClean**: Toggle Live cleanup channels, adjust deletion delays (in seconds), whitelist users/roles, or instantly purge up to 2000 messages.
  - **Wellbeing**: Adjust broadcast channels, configure min/max random hours intervals, or dispatch a test wellbeing warning box.
  - **Economy**: Configure default starting balances for new users, bulk-assign credit balances to every server member, or set payday rewards and cooldown timers.
- **Security Lock**: Command `/root` requires **Manage Guild** permissions. All buttons are locked strictly to the admin who opened the panel.

## Commands
*   `[p]root` (or `/root`) — Opens the Mainframe Command Center dashboard.
