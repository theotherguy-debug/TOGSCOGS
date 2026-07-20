# 👾 hijack

A button-based interactive console hacking game where players breach firewalls, deploy ice walls, and siphon credits from targets.

---

## Gameplay & Rules

### Hacking Breach (`[p]breachui`)
- Challenge a target player to an interactive terminal battle.
- The attacker must breach the target's firewall nodes before the trace timer completes.
- **Upgrades**:
  - **RAM Booster**: Accelerates processor rates to speed up breach actions.
  - **Icewall v2**: Strengthens firewall grids to slow down the attacker.
  - **Overdrive Signal**: Deploys malware anomalies to bypass protection.
- **Credit Stealing**:
  - **Attacker Wins**: Siphons `10%` of the defender's total bank balance (minimum 50 credits).
  - **Defender Wins (Secures Trace)**: Counter-siphons `10%` of the attacker's bank balance!

---

## Player Commands

*   **`[p]terminalui`** (or `/terminalui`) — Opens your personal hacker terminal console to view status and upgrades.
*   **`[p]breachui <member>`** (or `/breachui <member>`) — Initiates a direct hack breach request against a target member.
*   **`[p]hackstats`** — Shows your total successful hacks, defenses, rank, and unlocked achievements.

---

## Administrator Commands
Require **Manage Guild** or **Administrator** permissions.

*   **`[p]root`** (or `/root`) — Open the Mainframe Admin Dashboard to toggle global firewall lockdowns.
