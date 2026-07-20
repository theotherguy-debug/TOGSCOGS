# theothersequence

An ultimate high-stakes multi-channel sequence counting game for Red Discord Bot v3 with custom mathematical expression evaluation, cyberpunk themes, dynamic slash commands, server prestige rankings, PvP wagers, and hardcore Survivor Mode.

## Features
* **Multi-Channel Counting**: Run independent sequence counting games in different channels on the same server.
* **Math Expression Solver**: Accepts valid mathematical expressions (e.g. `2+2`, `12/3`, `5^2`) and evaluates them to determine if they match the next index.
* **Highest Progression Leaderboard**: Tracks users by the highest number they have successfully counted (rather than total counts).
* **Save Shields**: Protects your streak from breaking when a wrong number is submitted. Saves can be toggled on/off and priced separately per channel.
* **Economy Integration**: Optionally allow members to buy saves for a channel using their Red bank credits.
* **Cyberpunk Overlays**: Dynamic cyberpunk alerts, warning nodes, and system messages when games are won, saved, or lost.
* **Anti-Cheat Defenses**: Editing or deleting counted messages instantly triggers a game over event.
* **PvP Counting Duels (Speed Arenas)**: Challenge other players to wager-based counting shootouts in temporary threads. Features a 5-second response limit per turn and automated pot settlement.
* **Hardcore Survivor Mode**: Extreme stakes channels with no save shields, entry licensing/skill gates, season exiles, containment lockout roles, bank bankruptcy penalties, and milestone jackpot splits.
* **Startup Catch-Up Resync**: Automatically reads channel history when booting online, catching up on counts sent while the bot was offline and retroactively handling errors.

---

## Commands & Slash Options

Every command is a **hybrid command** (works as standard prefix commands like `[p]counting` or as slash commands like `/counting`).

### Member / Public Commands
* `/countlb` (Aliases: `clb`, `scoreboard`): View the highest sequence progression leaderboard.
* `/buysave [channel]` (Aliases: `bs`): Purchase a save token for a specific channel using server currency.
* `/buysurvivorlicense` (Aliases: `buysurv`): Purchase a lifetime license to type in Survivor-enabled channels.
* `/cduel challenge <opponent> <wager>`: Initiate a counting duel shootout with another player.
* `/cduel accept`: Accept a pending counting duel challenge (deducts wager immediately).
* `/cduel decline`: Reject a pending counting duel challenge.
* `/cduel status`: View all active duels running on the server.

### Admin Commands (Group `/counting` or `[p]counting`)
* `/counting addchannel <channel>` (Aliases: `addc`, `enable`): Activate the sequence game on a channel.
* `/counting removechannel <channel>` (Aliases: `removec`, `delchannel`, `disable`): Deactivate the sequence game on a channel.
* `/counting togglesaves <toggle> [channel]` (Aliases: `togglesave`, `ts`): Enable or disable saves for a specific channel.
* `/counting addsave <amount> [channel]` (Aliases: `givesave`, `as`): Manually add saves to a channel.
* `/counting addmilestone <number> <value> [channel]` (Aliases: `addm`, `setmilestone`): Map a number to a web image/GIF URL or a Discord Sticker ID.
* `/counting viewmilestones [channel]` (Aliases: `viewm`, `milestones`, `showmilestones`): Show all milestones configured in a channel.
* `/counting removemilestone <number> [channel]` (Aliases: `removem`, `delmilestone`): Remove a milestone from a channel.
* `/counting setcount <count> [channel]` (Aliases: `setc`, `setvalue`, `override`): Manually realign a channel's current count index.
* `/counting prestigetarget <target> [channel]` (Aliases: `ptarget`, `pt`): Set the number required to prestige.
* `/counting prestige [channel]` (Aliases: `ascend`, `p`): Reset the sequence and increase the channel's Prestige rank when the target is reached.
* `/counting economy <toggle> [channel]` (Aliases: `toggleeconomy`, `eco`): Toggle credit purchases of saves in a channel.
* `/counting saveprice <price> [channel]` (Aliases: `setprice`, `price`): Adjust the credit price of save tokens.
* `/counting penaltyname <name>` (Aliases: `pname`, `setpenaltyname`): Change the nickname applied to members who break the streak (Server-Wide).
* `/counting duration <hours>` (Aliases: `pduration`, `setduration`): Set the duration in hours that the nickname penalty lasts (Server-Wide).

### Admin Survivor Commands (Group `/counting survivor`)
* `/counting survivor addchannel <channel>`: Enable Survivor mode rules on a channel (bypasses saves entirely).
* `/counting survivor removechannel <channel>`: Revert a channel to standard counting rules.
* `/counting survivor setbankruptcy <percent>`: Customize the credit fine bankruptcy percentage on failure (default `50`).
* `/counting survivor setcontainment <hours>`: Set the mute duration in hours on failure (default `24`).
* `/counting survivor setexile <hours>`: Set the season exile ban duration in hours on failure (default `168`).
* `/counting survivor setfee <credits>`: Set the credit cost to buy a Survivor License (default `5000`).
* `/counting survivor setmincounts <counts>`: Set the minimum highest progression level required to enter (default `100`).
* `/counting survivor setrole <role>`: Assign a containment/mute role given to failing players.
* `/counting survivor config`: View all active Survivor configurations and jackpot status.

---

## Game Formats

### PvP Counting Duels
1. **Accepting a Duel** spawns a public thread `⚡-duel-PlayerA-vs-PlayerB` and locks wagers in place.
2. Players must count up sequentially (**1, 2, 3...**) taking alternating turns.
3. **Turn timer limit is 5.0 seconds**.
4. Double counting, wrong numbers, or timing out results in an instant defeat.
5. The victor receives the combined pot minus a **5% server tax**.
6. The thread is cleaned up and deleted 10 seconds post-match.

### Hardcore Survivor Channels
1. **Saves are ignored**; one error resets the channel and triggers penalties.
2. Breaking the streak results in:
   * **Credit Bankruptcy**: Deducts a customizable percentage of your wallet and puts it into the Jackpot Vault.
   * **Containment**: Monospace shamed name change and containment mute role applied.
   * **Exile**: Temp-banned from typing in the Survivor channel for a season duration.
3. Successfully reaching a milestone split-payout distributes the accumulated **Jackpot Vault** to active streak contributors proportionally.

---

## Installation
Copy the cog folder to your custom cogs directory and load it:
```bash
[p]cog load theothersequence
```
*(Make sure to sync slash commands with Discord: `[p]slash sync`)*
