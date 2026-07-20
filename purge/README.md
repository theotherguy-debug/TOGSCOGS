# AutoClean

An automated message cleanup utility for Red-DiscordBot that automatically purges messages in configured channels after a configurable delay.

## Features

- **Automated Deletion**: Periodically deletes messages in designated channels after a configurable delay (default is 1 hour).
- **Whitelisting**: Allow messages from specific users or roles to bypass the cleanup process.
- **On-Demand Purging**: Instantly purge up to 2000 messages in a channel.
- **Resource Management**: Automatically cleans up running tasks on unload to prevent memory leaks.

## Commands

All commands require **Administrator** permissions or the **Manage Messages** permission.

*   `[p]autoclean` (Alias: `[p]cleaner`)
    *   `toggle`: Enable or disable the automated cleanup engine for the current channel.
    *   `delay <seconds>`: Set the expiration delay in seconds (minimum: 5 seconds).
    *   `ignoreuser <member>`: Whitelist or un-whitelist a member from cleanup.
    *   `ignorerole <role>`: Whitelist or un-whitelist a role from cleanup.
    *   `clearnow [amount=100]`: Instantly purge up to 2000 messages in the current channel.
    *   `status`: Displays the current configuration status for the channel.

## Code Architecture

- **`on_message` Listener**: Monitors incoming messages in guild channels. If the channel has AutoClean enabled, the cog checks if the message author or their roles are whitelisted. If not, it spawns a deletion task.
- **Task Tracking**: Tasks are tracked in an internal set (`self._tracked_tasks`) to ensure they can be cleanly cancelled when the cog is unloaded via `cog_unload()`.
- **Configuration Storage**: Uses Red's `Config` system registered at the channel level.
