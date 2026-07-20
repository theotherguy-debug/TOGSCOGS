import random
import re
import discord
from redbot.core import commands, Config

# Monospace character conversion offsets
# A-Z: U+1D670 to U+1D689 (ord('A') = 65 -> 65 + 120367 = 120432)
# a-z: U+1D68A to U+1D6A3 (ord('a') = 97 -> 97 + 120361 = 120458)
# 0-9: U+1D7F6 to U+1D7FF (ord('0') = 48 -> 48 + 120774 = 120822)
def to_monospace(text: str) -> str:
    """Converts alphanumeric characters in text to monospace Unicode counterparts."""
    result = []
    for char in text:
        o = ord(char)
        if 65 <= o <= 90:  # A-Z
            result.append(chr(o + 120367))
        elif 97 <= o <= 122:  # a-z
            result.append(chr(o + 120361))
        elif 48 <= o <= 57:  # 0-9
            result.append(chr(o + 120774))
        else:
            result.append(char)
    return "".join(result)


def from_monospace(text: str) -> str:
    """Converts monospace Unicode characters back to standard alphanumeric characters."""
    result = []
    for char in text:
        o = ord(char)
        if 120432 <= o <= 120457:  # 𝙰-𝚉 (Mathematical Monospace Capital)
            result.append(chr(o - 120367))
        elif 120458 <= o <= 120483:  # 𝚊-𝚣 (Mathematical Monospace Small)
            result.append(chr(o - 120361))
        elif 120822 <= o <= 120831:  # 𝟶-𝟿 (Mathematical Monospace Digit)
            result.append(chr(o - 120774))
        else:
            result.append(char)
    return "".join(result)


THEME_PATTERNS = {
    "terminal": [
        "C:\\Users\\{name}",
        "C:\\user\\{name}",
        "{name}.py",
        "{name}.json",
        "{name}.exe",
        "{name}.sh",
        "{name}.bat",
        "{name}.js",
        "{name}.pyw",
        "{name}.cpp",
        "{name}.h",
        "{name}.go",
        "{name}.rs",
        "{name}.java",
        "{name}.class",
        "{name}.jar",
        "{name}.conf",
        "{name}.ini",
        "{name}.log",
        "{name}.cfg",
        "{name}.md",
        "{name}.txt",
        "root@{name}:~$",
        "{name}@localhost",
        "admin@{name}",
        "system@{name}",
        "./{name}",
        "./{name}.bin",
        "usr/bin/{name}",
        "usr/local/bin/{name}",
        "bin/{name}",
        "/home/{name}",
        "~/{name}",
        "cmd/{name}",
        "sudo rm -rf {name}",
        "git clone {name}",
        "npm i {name}",
        "pip install {name}",
        "docker run {name}",
        "nano ~/{name}",
        "grep -r {name}",
        "alias {name}='run'",
        "cat {name}.txt",
        "make build-{name}",
        "history | grep {name}",
    ],
    "virus": [
        "Trojan.Win32.{name}",
        "Worm.{name}",
        "Ransomware.{name}",
        "Adware.{name}",
        "Keylogger.{name}",
        "Spyware.{name}",
        "Backdoor.{name}",
        "Rootkit.{name}",
        "Exploit.{name}",
        "Malware.{name}",
        "WannaCry.{name}",
        "ILOVEYOU.{name}",
        "Stuxnet.{name}",
        "Petya.{name}",
        "Conficker.{name}",
        "MyDoom.{name}",
        "Sasser.{name}",
        "CodeRed.{name}",
        "Melissa.{name}",
        "Zeus.{name}",
        "CryptoLocker.{name}",
        "Sobig.{name}",
        "Slammer.{name}",
        "Blaster.{name}",
        "Agent.{name}.tmp",
        "ZeroDay.{name}",
        "Exploit.CVE-{name}",
        "Spy.Pegasus.{name}",
        "Backdoor.ShadowBrokers.{name}",
        "Ransom.Locky.{name}",
        "Trojan.JS.{name}",
        "Trojan.Android.{name}",
        "Stealer.Redline.{name}",
        "Botnet.Mirai.{name}",
        "C2.Server.{name}",
    ],
    "database": [
        "SELECT * FROM {name}",
        "db.users.find({name})",
        "key:user:{name}",
        "INSERT INTO {name}",
        "redis.get({name})",
        "mongodb.{name}",
        "postgres.public.{name}",
        "sqlite3.db.{name}",
        "UPDATE users SET name={name}",
        "DELETE FROM {name}",
        "cache:session:{name}",
        "table:{name}",
        "ROW_ID_{name}",
        "idx_{name}_name",
        "SHOW TABLES LIKE '{name}'",
        "db.auth({name})",
        "redis.hgetall({name})",
        "SELECT COUNT({name})",
        "neo4j.match({name})",
        "db.dropDatabase({name})",
        "ALTER TABLE {name}",
        "schema:graphql:{name}",
        "query_lock_{name}",
        "deadlock_{name}",
    ],
    "network": [
        "127.0.0.1/{name}",
        "192.168.1.{name}",
        "https://{name}",
        "ssh://{name}",
        "ftp://{name}",
        "{name}:8080",
        "{name}:443",
        "ping.{name}",
        "dns.lookup.{name}",
        "subdomain.{name}.com",
        "localhost:{name}",
        "ipconfig/release/{name}",
        "traceroute.{name}",
        "packet_loss_{name}",
        "gateway_{name}",
        "tor.node.{name}",
        "vpn.tunnel.{name}",
        "ssl.handshake.{name}",
        "port_scan_{name}",
        "nslookup.{name}",
        "dhcp_lease_{name}",
        "arp_table_{name}",
        "subnet_mask_{name}",
        "wireshark_cap_{name}",
    ],
    "system": [
        "dev/sda1/{name}",
        "/dev/null/{name}",
        "sys/bus/usb/{name}",
        "{name}.sys",
        "{name}.dll",
        "kernel_panic_{name}",
        "IRQ_CONFLICT_{name}",
        "C:\\Windows\\System32\\{name}",
        "sys/kernel/{name}",
        "mnt/c/Users/{name}",
        "boot_sect_{name}",
        "cpu_usage_{name}%",
        "ram_alloc_{name}",
        "systemd-service-{name}",
        "regedit.{name}",
        "bsod_dump_{name}",
        "system.log.{name}",
        "init.d/{name}",
        "C:\\Temp\\{name}",
        "process_id_{name}",
        "thread_lock_{name}",
        "core_dump_{name}",
        "sysctl.conf.{name}",
        "cron.d/{name}",
    ]
}

# Compile patterns for base name extraction across all themes
PATTERNS_REGEX = []
for plist in THEME_PATTERNS.values():
    for p in plist:
        escaped = re.escape(p).replace(r"\{name\}", r"(.+)")
        PATTERNS_REGEX.append(re.compile(f"^{escaped}$", re.IGNORECASE))


def clean_nickname(nick: str) -> str:
    """Extracts original name from any terminal/theme styled string."""
    if not nick:
        return ""
    normal = from_monospace(nick)
    for rx in PATTERNS_REGEX:
        match = rx.match(normal)
        if match:
            return match.group(1)
    return normal


class SysNames(commands.Cog):
    """Formats Discord server nicknames into terminal-themed and script-themed styles."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=89234892374, force_registration=True)
        default_guild = {
            "enabled": False,
            "theme": "all",
        }
        self.config.register_guild(**default_guild)

    def _apply_terminal_style(self, name: str, pattern: str) -> str:
        """Helper to safely format a name into a terminal pattern keeping under the 32-character limit."""
        # Calculate maximum characters allowed for the name portion
        empty_pattern_len = len(pattern.format(name=""))
        max_len = 32 - empty_pattern_len
        if max_len < 1:
            max_len = 1
        
        truncated = name[:max_len]
        formatted = pattern.format(name=truncated)
        return to_monospace(formatted)

    async def _format_and_set_nickname(self, member: discord.Member) -> bool:
        """Formats and attempts to set the member's nickname. Returns True on success."""
        guild = member.guild
        me = guild.me
        
        # Verify Manage Nicknames permissions
        if not me.guild_permissions.manage_nicknames:
            return False
            
        # Verify hierarchy
        if member.top_role >= me.top_role or member == guild.owner:
            return False
            
        # Select pattern based on guild theme setting
        theme = await self.config.guild(guild).theme()
        if theme == "all" or theme not in THEME_PATTERNS:
            patterns_pool = []
            for plist in THEME_PATTERNS.values():
                patterns_pool.extend(plist)
        else:
            patterns_pool = THEME_PATTERNS[theme]

        pattern = random.choice(patterns_pool)
        
        # Use preferred nickname (if set), global display name, or username
        current_display = member.nick or member.global_name or member.name
        name_to_use = clean_nickname(current_display)
        if not name_to_use:
            name_to_use = member.global_name or member.name
            
        formatted_nick = self._apply_terminal_style(name_to_use, pattern)
        
        try:
            await member.edit(nick=formatted_nick)
            return True
        except discord.HTTPException:
            return False

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Automatically formats a member's nickname when they join, if enabled."""
        guild = member.guild
        if member.bot:
            return
            
        if not await self.config.guild(guild).enabled():
            return
            
        await self._format_and_set_nickname(member)

    @commands.group(name="terminalnames")
    @commands.guild_only()
    @commands.admin_or_permissions(manage_nicknames=True)
    async def terminalnames(self, ctx):
        """Manage terminal nickname formatting settings."""
        pass

    @terminalnames.command(name="toggle")
    async def toggle(self, ctx):
        """Toggle automatic terminal formatting on member join."""
        current = await self.config.guild(ctx.guild).enabled()
        await self.config.guild(ctx.guild).enabled.set(not current)
        status = "enabled" if not current else "disabled"
        await ctx.send(f"Terminal nickname formatting on join is now **{status}**.")

    @terminalnames.command(name="theme")
    async def theme(self, ctx, theme_name: str = None):
        """Set the active formatting theme.
        
        Themes: all, terminal, virus, database, network, system
        """
        valid_themes = ["all"] + list(THEME_PATTERNS.keys())
        if not theme_name or theme_name.lower() not in valid_themes:
            options = ", ".join(valid_themes)
            await ctx.send(f"⚠️ Invalid theme name. Please choose from: **{options}**")
            return
            
        theme_to_set = theme_name.lower()
        await self.config.guild(ctx.guild).theme.set(theme_to_set)
        await ctx.send(f"✅ Active formatting theme has been set to: **{theme_to_set}**")

    @terminalnames.command(name="formatall")
    async def formatall(self, ctx):
        """Format all eligible server members' nicknames."""
        async with ctx.typing():
            guild = ctx.guild
            me = guild.me
            
            if not me.guild_permissions.manage_nicknames:
                await ctx.send("I do not have the **Manage Nicknames** permission.")
                return
                
            success_count = 0
            fail_count = 0
            skipped_count = 0
            
            for member in guild.members:
                if member.bot:
                    skipped_count += 1
                    continue
                if member.top_role >= me.top_role or member == guild.owner:
                    skipped_count += 1
                    continue
                    
                res = await self._format_and_set_nickname(member)
                if res:
                    success_count += 1
                else:
                    fail_count += 1
                    
            await ctx.send(
                f"Nickname formatting complete!\n"
                f"- Formatted: **{success_count}** members\n"
                f"- Skipped (hierarchy/bot/owner): **{skipped_count}**\n"
                f"- Failed: **{fail_count}**"
            )

    @terminalnames.command(name="formatmember")
    async def formatmember(self, ctx, member: discord.Member):
        """Format a specific member's nickname."""
        guild = ctx.guild
        me = guild.me
        if not me.guild_permissions.manage_nicknames:
            await ctx.send("I do not have the **Manage Nicknames** permission.")
            return
        if member.top_role >= me.top_role or member == guild.owner:
            await ctx.send("I cannot format this member's nickname due to hierarchy or ownership constraints.")
            return
            
        res = await self._format_and_set_nickname(member)
        if res:
            await ctx.send(f"Formatted nickname for {member.mention}.")
        else:
            await ctx.send(f"Failed to change nickname for {member.mention}.")

    @terminalnames.command(name="resetall")
    async def resetall(self, ctx):
        """Reset all eligible server members' nicknames back to default (clears nickname)."""
        async with ctx.typing():
            guild = ctx.guild
            me = guild.me
            
            if not me.guild_permissions.manage_nicknames:
                await ctx.send("I do not have the **Manage Nicknames** permission.")
                return
                
            success_count = 0
            fail_count = 0
            skipped_count = 0
            
            for member in guild.members:
                if not member.nick:
                    skipped_count += 1
                    continue
                if member.bot:
                    skipped_count += 1
                    continue
                if member.top_role >= me.top_role or member == guild.owner:
                    skipped_count += 1
                    continue
                    
                try:
                    await member.edit(nick=None)
                    success_count += 1
                except discord.HTTPException:
                    fail_count += 1
                    
            await ctx.send(
                f"Nickname reset complete!\n"
                f"- Reset: **{success_count}** members\n"
                f"- Skipped (no nickname/hierarchy/bot/owner): **{skipped_count}**\n"
                f"- Failed: **{fail_count}**"
            )

    @terminalnames.command(name="status")
    async def status(self, ctx):
        """Show the current settings and status of the terminalnames cog."""
        enabled = await self.config.guild(ctx.guild).enabled()
        theme = await self.config.guild(ctx.guild).theme()
        status_text = "Enabled" if enabled else "Disabled"
        
        embed = discord.Embed(
            title="TerminalNames Settings",
            description=f"Auto-formatting on join: **{status_text}**\nActive Theme: **{theme}**",
            color=discord.Color.green() if enabled else discord.Color.red()
        )
        total_patterns = sum(len(x) for x in THEME_PATTERNS.values())
        embed.add_field(name="Theme Patterns available", value=f"Total: **{total_patterns}** patterns across **{len(THEME_PATTERNS)}** themes.", inline=False)
        embed.add_field(
            name="Sample Formats", 
            value="`𝙲:\\𝚄𝚜𝚎𝚛𝚜\\a𝚗𝚍𝚛𝚎𝚠` (Terminal)\n`𝚃𝚛𝚘𝚓𝚊𝚗.𝚆𝚒𝚗𝟹𝟸.a𝚗𝚍𝚛𝚎𝚠` (Virus)\n`𝚍𝚋.𝚞𝚜𝚎𝚛𝚜.𝚏𝚒𝚗𝚍(a𝚗𝚍𝚛𝚎𝚠)` (Database)\n`𝟷𝟸𝟽.𝟶.𝟶.𝟷/a𝚗𝚍𝚛𝚎𝚠` (Network)", 
            inline=False
        )
        await ctx.send(embed=embed)
