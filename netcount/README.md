# 🔢 netcount

The ultimate sequence counting game built for Redbot. It includes wager duels, standard channel counting, and extreme Hardcore Survivor nodes.

---

## Rules & How to Play

### 1. Standard Counting Channel
- **Goal**: Work as a team to count up from `1` sequentially (`1`, `2`, `3`...).
- **Rule**: You **cannot** count twice in a row. Someone else must input the next number.
- **Wagers**: If enabled, players can spend credits to purchase save tokens to protect the streak.

### 2. PvP Duels (`[p]cduel`)
- **Stakes**: Challenge another user to a live sequence-counting speed battle for server credits!
- **Gameplay**:
  - Once the duel is accepted, the system opens a temporary thread arena.
  - The **5-second turn timer** starts only after the first count (the number 1) is typed.
  - Players must type the next sequence number within their 5-second turn window.
  - If a player inputs a wrong number, types twice in a row, or lets the timer hit `0`, they fail and the opponent wins the credit wager!

### 3. Hardcore Survivor Mode
- **Stakes**: Extremely high-stakes counting node designed for advanced operators.
- **Entry Gate**: Requires a minimum regular sequence contribution score and a purchased lifetime **Survivor License** (default: `5,000` credits).
- **Rules**:
  - **No Saves**: Save tokens cannot be used here. One mistake resets the streak to 0.
  - **Exile & Containment**: The player who makes a mistake is shamed with a custom nickname, stripped of their access roles, and exiled from the channel for `168 hours` (7 days).
  - **Bankruptcy**: The failing player is fined `50%` of their entire credit balance, which is split as a jackpot among the players who contributed to the current streak.

---

## Player Commands

### ⚔️ PvP Counting Duels (`cduel` group)
*   **`[p]cduel challenge <member> [wager]`** — Challenges a player to a live sequence battle with an optional credit wager.
*   **`[p]cduel accept`** — Accepts a pending duel challenge (opens thread, deducts wagers).
*   **`[p]cduel decline`** — Rejects a pending duel challenge.
*   **`[p]cduel status`** — Displays active duels on the server.

### 🛡️ Shields & Licenses
*   **`[p]buysave [channel]`** (Alias: `[p]bs`) — Purchases a backup save token for a channel.
*   **`[p]buysurvivorlicense`** (Alias: `[p]buysurv`) — Purchases a lifetime license to access Survivor channels.

### 🏆 Scores & Leaderboards
*   **`[p]countlb`** (Aliases: `[p]clb`, `[p]scoreboard`) — Displays the top 10 players on the server.

---

## Administrator Commands
Require **Manage Guild** permissions.

*   **`[p]counting addchannel <channel>`** — Enable sequence counting in a channel.
*   **`[p]counting removechannel <channel>`** — Disable counting and wipe channel logs.
*   **`[p]counting setcount <number> [channel]`** — Manually override/set the current count.
*   **`[p]counting survivor`** — Sub-command group to configure Survivor Mode (fees, bankruptcy %, exile times).
*   **`[p]root`** (or `/root`) — Opens the Mainframe Admin Dashboard to configure everything via buttons.
