# TerminalNames

A Red-DiscordBot utility that automatically or manually formats server members' nicknames into terminal-themed strings (e.g., file paths, prompt inputs, script files) using unicode monospace characters for font continuity.

## Features

- **Monospace Font Mapping**: Converts standard alphanumeric characters (`A-Z`, `a-z`, `0-9`) into mathematical monospace equivalents to preserve the look and feel of a system console across all names.
- **Themed Styling Assortment**: Includes a massive pool of preconfigured naming conventions split across multiple themes:
  - **terminal**: Command prompts and file extensions (e.g. `C:\Users\username`, `username.py`, `root@username:~$`).
  - **virus**: Known malware and system infections (e.g. `Trojan.Win32.username`, `WannaCry.username`, `ILOVEYOU.username`, `Stuxnet.username`).
  - **database**: SQL and Key-Value structures (e.g. `SELECT * FROM username`, `db.users.find(username)`).
  - **network**: IP addresses and networking protocols (e.g. `127.0.0.1/username`, `https://username`).
  - **system**: System kernel directories and drivers (e.g. `dev/sda1/username`, `username.sys`).
  - **all**: Dynamically blends all themes together, selecting randomly from the entire listing.
- **Join Automation**: When enabled, new members are assigned a randomized style automatically when they join the server.
- **Bulk Administrative Management**: Provides commands to format the entire server's eligible members at once, format specific members, or toggle join-based formatting.
- **Discord Character Limits Guard**: Automatically truncates the username parameter before formatting to guarantee that the final nickname never exceeds Discord's 32-character boundary, preventing API errors.

## Commands

Commands require **Administrator** permissions or the **Manage Nicknames** permission.

*   `[p]terminalnames`
    *   `toggle`: Toggles whether new members are automatically formatted upon joining.
    *   `theme <theme_name>`: Sets the active theme. Options: `all`, `terminal`, `virus`, `database`, `network`, `system`.
    *   `formatall`: Iterates through all server members and formats their nicknames (skips bots, the server owner, and members with roles equal to or higher than the bot).
    *   `formatmember <member>`: Instantly formats a specific target member's nickname.
    *   `resetall`: Resets all server members' nicknames back to default (clears nickname).
    *   `status`: Displays current configuration settings and a list of sample formats.
