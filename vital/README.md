# WellBeing Reminders

A Red-DiscordBot utility that sends cheekily hostile, terminal-themed well-being reminders to designated channels at randomized intervals. The alerts automatically delete after a specified period to avoid cluttering chat history.

## Features

-   **Variable Broadcast Loop**: Reminders are sent out on a random timer configured within minimum and maximum boundaries (e.g., every 3 to 6 hours).
-   **Terminal Aesthetics**: Well-being warnings are formatted with simulated "System Compromise" ASCII structures warning about dehydration, poor posture, screen staring, or lack of hygiene.
-   **Auto-Cleanup**: Dispatched reminders automatically delete themselves (by default after 24 hours) to prevent channels from becoming clogged.
-   **Configurable Alert Pool**: Combines built-in hardcoded messages, external JSON alerts (`alerts.json`), and custom server-specific alerts.

## Commands

Require **Administrator** permissions or the **Manage Guild** permission.

*   `[p]system` (Alias: `[p]sys`)
    *   `addchannel`: Adds the current text channel to the broadcast list.
    *   `interval <min_hours> <max_hours>`: Sets the minimum and maximum random intervals (in hours) between alerts.
    *   `addalert <text>`: Adds a custom well-being alert string to the rotation.
    *   `removealert <index>`: Removes a custom alert from rotation by its index.
    *   `test`: Immediately broadcasts a random well-being reminder to the current channel which self-deletes after 5 minutes.

## Under the Hood

-   **Interval Scheduling**: Updates the reminder loop dynamically when changing wait ranges by modifying `reminder_loop.change_interval()`.
-   **Config Registry**: Stores whitelisted target broadcast channels, custom alert texts, and min/max wait durations using Red's global `Config` schema.
-   **Auto-Deletion**: Spawns non-blocking tasks (`delete_after()`) to handle message deletion without stalling the core event queue.
