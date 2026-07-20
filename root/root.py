import discord
import asyncio
import time
from typing import Optional, List
from redbot.core import commands, Config, bank
from discord import ui

# --- ANSI Terminal Colors ---
RED = "\u001b[1;31m"
GREEN = "\u001b[1;32m"
YELLOW = "\u001b[1;33m"
CYAN = "\u001b[1;36m"
WHITE = "\u001b[1;37m"
RESET = "\u001b[0m"


class Root(commands.Cog):
    """Unified Operator Mainframe Control Panel for all gaming subsystems."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=9847382741, force_registration=True)

    @commands.hybrid_command(name="root")
    @commands.guild_only()
    @commands.admin_or_permissions(manage_guild=True)
    async def root(self, ctx: commands.Context):
        """Open the unified administrative terminal mainframe panel."""
        view = MainframeMainView(self.bot, ctx.author)
        embed = view.get_main_embed()
        message = await ctx.send(embed=embed, view=view)
        view.message = message


class MainframeMainView(ui.View):
    def __init__(self, bot, author):
        super().__init__(timeout=300)
        self.bot = bot
        self.author = author
        self.message = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ You are not authorized to control this terminal mainframe.", ephemeral=True)
            return False
        return True

    def get_main_embed(self) -> discord.Embed:
        desc = (
            f"```ansi\n"
            f"{CYAN}╔══════════════════════════════════════════════════════╗{RESET}\n"
            f"{CYAN}║            MAINFRAME OPERATOR MAIN PANEL             ║{RESET}\n"
            f"{CYAN}╚══════════════════════════════════════════════════════╝{RESET}\n\n"
            f" [STATUS]: {GREEN}🟢 SYSTEM MATRIX ONLINE{RESET}\n"
            f" [ACCESS]: {GREEN}GRANTED / ADMIN LEVEL{RESET}\n\n"
            f" Select a subsystem below to begin configuration edits.\n"
            f"```"
        )
        embed = discord.Embed(title="⚙️ Mainframe Admin Control Panel", description=desc, color=discord.Color.dark_blue())
        embed.set_footer(text="Central Command Terminal • Author Only")
        return embed

    @ui.button(label="Counting System", style=discord.ButtonStyle.primary, emoji="🔢", row=0)
    async def counting_btn(self, interaction: discord.Interaction, button: ui.Button):
        cog = self.bot.get_cog("NetCount")
        if not cog:
            return await interaction.response.send_message("❌ Subsystem offline. NetCount cog is not loaded.", ephemeral=True)
        view = CountingSubsystemView(self.bot, self.author, cog, self, interaction.guild)
        await interaction.response.edit_message(embed=view.get_embed(), view=view)

    @ui.button(label="Nicknames", style=discord.ButtonStyle.primary, emoji="🏷️", row=0)
    async def nicknames_btn(self, interaction: discord.Interaction, button: ui.Button):
        cog = self.bot.get_cog("SysNames")
        if not cog:
            return await interaction.response.send_message("❌ Subsystem offline. SysNames cog is not loaded.", ephemeral=True)
        view = NicknameSubsystemView(self.bot, self.author, cog, self)
        await interaction.response.edit_message(embed=view.get_embed(), view=view)

    @ui.button(label="Hacking UI", style=discord.ButtonStyle.primary, emoji="👾", row=0)
    async def hacking_btn(self, interaction: discord.Interaction, button: ui.Button):
        cog = self.bot.get_cog("Hijack")
        if not cog:
            return await interaction.response.send_message("❌ Subsystem offline. Hijack cog is not loaded.", ephemeral=True)
        view = HackingSubsystemView(self.bot, self.author, cog, self)
        await interaction.response.edit_message(embed=view.get_embed(), view=view)

    @ui.button(label="AutoClean", style=discord.ButtonStyle.secondary, emoji="🧹", row=1)
    async def autoclean_btn(self, interaction: discord.Interaction, button: ui.Button):
        cog = self.bot.get_cog("Purge")
        if not cog:
            return await interaction.response.send_message("❌ Subsystem offline. Purge cog is not loaded.", ephemeral=True)
        view = AutoCleanSubsystemView(self.bot, self.author, cog, self, interaction.guild)
        await interaction.response.edit_message(embed=view.get_embed(), view=view)

    @ui.button(label="Wellbeing alerts", style=discord.ButtonStyle.secondary, emoji="🏥", row=1)
    async def wellbeing_btn(self, interaction: discord.Interaction, button: ui.Button):
        cog = self.bot.get_cog("Vital")
        if not cog:
            return await interaction.response.send_message("❌ Subsystem offline. Vital cog is not loaded.", ephemeral=True)
        view = WellbeingSubsystemView(self.bot, self.author, cog, self, interaction.guild)
        await interaction.response.edit_message(embed=view.get_embed(), view=view)

    @ui.button(label="Economy & Bank", style=discord.ButtonStyle.success, emoji="💰", row=2)
    async def economy_btn(self, interaction: discord.Interaction, button: ui.Button):
        view = EconomySubsystemView(self.bot, self.author, self)
        await interaction.response.edit_message(embed=view.get_embed(), view=view)

    @ui.button(label="Exit Matrix", style=discord.ButtonStyle.danger, emoji="❌", row=2)
    async def exit_btn(self, interaction: discord.Interaction, button: ui.Button):
        for item in self.children:
            item.disabled = True
        desc = "```ansi\n [LOG]: Connection to Mainframe safely terminated.\n```"
        embed = discord.Embed(title="❌ Terminated Connection", description=desc, color=discord.Color.dark_red())
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()


# =====================================================================
#                      COUNTING SUBSYSTEM VIEW
# =====================================================================
class CountingSubsystemView(ui.View):
    def __init__(self, bot, author, cog, parent_view, guild):
        super().__init__(timeout=180)
        self.bot = bot
        self.author = author
        self.cog = cog
        self.parent_view = parent_view
        self.selected_channel_id = None
        
        menu = ChannelSelectMenu(self)
        menu._populate_channels(guild)
        self.add_item(menu)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Unauthorized.", ephemeral=True)
            return False
        return True

    def get_embed(self) -> discord.Embed:
        desc = (
            f"```ansi\n"
            f"{YELLOW}╔══════════════════════════════════════════════════════╗{RESET}\n"
            f"{YELLOW}║            🔢 SEQUENCE COUNTING SUBSYSTEM            ║{RESET}\n"
            f"{YELLOW}╚══════════════════════════════════════════════════════╝{RESET}\n\n"
            f" Configure wagers, licenses, and survivor rules here.\n"
            f" Select a channel from the dropdown to unlock actions.\n"
            f" Selected Channel ID: {self.selected_channel_id or 'None'}\n"
            f"```"
        )
        return discord.Embed(title="Subsystem: Sequence Counting", description=desc, color=discord.Color.orange())

    @ui.button(label="Toggle Counting", style=discord.ButtonStyle.primary, row=1)
    async def toggle_counting(self, interaction: discord.Interaction, button: ui.Button):
        if not self.selected_channel_id:
            return await interaction.response.send_message("❌ Please select a channel first.", ephemeral=True)
        guild = interaction.guild
        ch_str = str(self.selected_channel_id)
        async with self.cog.config.guild(guild).channels() as channels:
            if ch_str in channels:
                channels.pop(ch_str)
                msg = f"Disabled counting in <#{ch_str}>."
            else:
                channels[ch_str] = self.cog.get_default_channel_config()
                msg = f"Enabled counting in <#{ch_str}>."
        await interaction.response.send_message(f"✅ {msg}", ephemeral=True)

    @ui.button(label="Toggle Survivor Mode", style=discord.ButtonStyle.primary, row=1)
    async def toggle_survivor(self, interaction: discord.Interaction, button: ui.Button):
        if not self.selected_channel_id:
            return await interaction.response.send_message("❌ Please select a channel first.", ephemeral=True)
        guild = interaction.guild
        ch_str = str(self.selected_channel_id)
        
        # Ensure it is at least an active counting channel
        channels = await self.cog.config.guild(guild).channels()
        if ch_str not in channels:
            async with self.cog.config.guild(guild).channels() as active_channels:
                active_channels[ch_str] = self.cog.get_default_channel_config()

        async with self.cog.config.guild(guild).survivor_channels() as surv_channels:
            if ch_str in surv_channels:
                surv_channels.pop(ch_str)
                msg = f"Disabled Survivor rules on <#{ch_str}>."
            else:
                surv_channels[ch_str] = True
                msg = f"Enabled Survivor rules on <#{ch_str}> (Saves disabled, extreme stakes active)."
        await interaction.response.send_message(f"💀 {msg}", ephemeral=True)

    @ui.button(label="Set Rules (Fee/Bankrupt %)", style=discord.ButtonStyle.secondary, row=2)
    async def set_rules(self, interaction: discord.Interaction, button: ui.Button):
        modal = CountingRulesModal(self.cog, interaction.guild)
        await interaction.response.send_modal(modal)

    @ui.button(label="Main Menu", style=discord.ButtonStyle.danger, emoji="⬅️", row=2)
    async def back(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.edit_message(embed=self.parent_view.get_main_embed(), view=self.parent_view)


class ChannelSelectMenu(ui.Select):
    def __init__(self, parent_view):
        self.parent_view = parent_view
        super().__init__(placeholder="Select a channel...", min_values=1, max_values=1, row=0)

    async def callback(self, interaction: discord.Interaction):
        self.parent_view.selected_channel_id = self.values[0]
        await interaction.response.edit_message(embed=self.parent_view.get_embed(), view=self.parent_view)

    def _populate_channels(self, guild: discord.Guild):
        self.options = []
        for ch in guild.text_channels[:25]:
            self.options.append(discord.SelectOption(label=ch.name, value=str(ch.id)))


class CountingRulesModal(ui.Modal, title="Configure Counting Settings"):
    fee = ui.TextInput(label="License Fee (Credits)", default="5000", placeholder="Integer cost")
    bankruptcy = ui.TextInput(label="Bankruptcy Percent (0-100)", default="50", placeholder="Integer percent")
    exile = ui.TextInput(label="Exile Duration (Hours)", default="168", placeholder="Duration to ban failing user")

    def __init__(self, cog, guild):
        super().__init__()
        self.cog = cog
        self.guild = guild

    async def on_submit(self, interaction: discord.Interaction):
        try:
            f = int(str(self.fee))
            b = int(str(self.bankruptcy))
            e = int(str(self.exile))
            if not (0 <= b <= 100):
                return await interaction.response.send_message("❌ Bankruptcy percent must be 0 to 100.", ephemeral=True)
            await self.cog.config.guild(self.guild).survivor_license_fee.set(f)
            await self.cog.config.guild(self.guild).survivor_bankruptcy_percent.set(b)
            await self.cog.config.guild(self.guild).survivor_exile_hours.set(e)
            await interaction.response.send_message("✅ Settings updated successfully.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Failed: Inputs must be integers.", ephemeral=True)


# =====================================================================
#                      NICKNAME SUBSYSTEM VIEW
# =====================================================================
class NicknameSubsystemView(ui.View):
    def __init__(self, bot, author, cog, parent_view):
        super().__init__(timeout=180)
        self.bot = bot
        self.author = author
        self.cog = cog
        self.parent_view = parent_view
        self.add_item(ThemeSelectMenu(self))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Unauthorized.", ephemeral=True)
            return False
        return True

    def get_embed(self) -> discord.Embed:
        desc = (
            f"```ansi\n"
            f"{GREEN}╔══════════════════════════════════════════════════════╗{RESET}\n"
            f"{GREEN}║            🏷️ NICKNAME FORMATTING COG                ║{RESET}\n"
            f"{GREEN}╚══════════════════════════════════════════════════════╝{RESET}\n\n"
            f" Configure nickname themes and trigger resets.\n"
            f" Choose a theme from the dropdown to update it server-wide.\n"
            f"```"
        )
        return discord.Embed(title="Subsystem: Nicknames", description=desc, color=discord.Color.green())

    @ui.button(label="Reset All Nicknames", style=discord.ButtonStyle.primary, row=1)
    async def reset_all(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        count = 0
        from sysnames.sysnames import clean_nickname
        for m in guild.members:
            if m.bot:
                continue
            original = clean_nickname(m.display_name)
            if original != m.display_name:
                try:
                    await m.edit(nick=original)
                    count += 1
                except discord.Forbidden:
                    pass
        await interaction.followup.send(f"✅ Reset {count} user nicknames successfully.", ephemeral=True)

    @ui.button(label="Main Menu", style=discord.ButtonStyle.danger, emoji="⬅️", row=2)
    async def back(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.edit_message(embed=self.parent_view.get_main_embed(), view=self.parent_view)


class ThemeSelectMenu(ui.Select):
    def __init__(self, parent_view):
        self.parent_view = parent_view
        super().__init__(placeholder="Select Name Theme...", min_values=1, max_values=1, row=0)
        self.options = [
            discord.SelectOption(label="Terminal Theme (e.g. name.py)", value="terminal"),
            discord.SelectOption(label="Virus Theme (e.g. name.exe)", value="virus"),
            discord.SelectOption(label="Database Theme (e.g. db_name)", value="database"),
            discord.SelectOption(label="System Theme (e.g. systemd-name)", value="system"),
            discord.SelectOption(label="Network Theme (e.g. ip_name)", value="network"),
            discord.SelectOption(label="Random Theme", value="all")
        ]

    async def callback(self, interaction: discord.Interaction):
        theme = self.values[0]
        guild = interaction.guild
        await self.parent_view.cog.config.guild(guild).theme.set(theme)
        await interaction.response.send_message(f"✅ Theme updated to **{theme}** server-wide.", ephemeral=True)


# =====================================================================
#                      HACKING SUBSYSTEM VIEW
# =====================================================================
class HackingSubsystemView(ui.View):
    def __init__(self, bot, author, cog, parent_view):
        super().__init__(timeout=180)
        self.bot = bot
        self.author = author
        self.cog = cog
        self.parent_view = parent_view

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Unauthorized.", ephemeral=True)
            return False
        return True

    def get_embed(self) -> discord.Embed:
        desc = (
            f"```ansi\n"
            f"{RED}╔══════════════════════════════════════════════════════╗{RESET}\n"
            f"{RED}║            👾 HACKING console COG                    ║{RESET}\n"
            f"{RED}╚══════════════════════════════════════════════════════╝{RESET}\n\n"
            f" Toggle network lockdowns and trace protocols.\n"
            f"```"
        )
        return discord.Embed(title="Subsystem: Hacking System", description=desc, color=discord.Color.red())

    @ui.button(label="Toggle Firewall Lockdown", style=discord.ButtonStyle.primary, row=0)
    async def toggle_lockdown(self, interaction: discord.Interaction, button: ui.Button):
        self.cog.lockdown_active = not self.cog.lockdown_active
        status = "ACTIVE / BLOCKING BREACHES" if self.cog.lockdown_active else "OFFLINE / NORMAL"
        await interaction.response.send_message(f"⚠️ Global lockdown state set to: **{status}**.", ephemeral=True)

    @ui.button(label="Main Menu", style=discord.ButtonStyle.danger, emoji="⬅️", row=1)
    async def back(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.edit_message(embed=self.parent_view.get_main_embed(), view=self.parent_view)


# =====================================================================
#                      AUTOCLEAN SUBSYSTEM VIEW
# =====================================================================
class AutoCleanSubsystemView(ui.View):
    def __init__(self, bot, author, cog, parent_view, guild):
        super().__init__(timeout=180)
        self.bot = bot
        self.author = author
        self.cog = cog
        self.parent_view = parent_view
        self.selected_channel_id = None
        
        menu = AutoCleanChannelSelectMenu(self)
        menu._populate_channels(guild)
        self.add_item(menu)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Unauthorized.", ephemeral=True)
            return False
        return True

    def get_embed(self) -> discord.Embed:
        desc = (
            f"```ansi\n"
            f"{WHITE}╔══════════════════════════════════════════════════════╗{RESET}\n"
            f"{WHITE}║            🧹 AUTOCLEAN SUBSYSTEM                    ║{RESET}\n"
            f"{WHITE}╚══════════════════════════════════════════════════════╝{RESET}\n\n"
            f" Manage real-time channel message purges.\n"
            f" Selected Channel ID: {self.selected_channel_id or 'None'}\n"
            f"```"
        )
        return discord.Embed(title="Subsystem: AutoClean", description=desc, color=discord.Color.light_grey())

    @ui.button(label="Toggle Clean", style=discord.ButtonStyle.primary, row=1)
    async def toggle_clean(self, interaction: discord.Interaction, button: ui.Button):
        if not self.selected_channel_id:
            return await interaction.response.send_message("❌ Please select a channel first.", ephemeral=True)
        channel = self.bot.get_channel(int(self.selected_channel_id))
        if not channel:
            return await interaction.response.send_message("❌ Channel not found.", ephemeral=True)
        
        current = await self.cog.config.channel(channel).enabled()
        await self.cog.config.channel(channel).enabled.set(not current)
        status = "ENABLED" if not current else "DISABLED"
        await interaction.response.send_message(f"🧹 AutoClean live purge in <#{channel.id}> set to **{status}**.", ephemeral=True)

    @ui.button(label="Set Purge Delay", style=discord.ButtonStyle.secondary, row=1)
    async def set_delay(self, interaction: discord.Interaction, button: ui.Button):
        if not self.selected_channel_id:
            return await interaction.response.send_message("❌ Please select a channel first.", ephemeral=True)
        channel = self.bot.get_channel(int(self.selected_channel_id))
        modal = AutoCleanDelayModal(self.cog, channel)
        await interaction.response.send_modal(modal)

    @ui.button(label="Main Menu", style=discord.ButtonStyle.danger, emoji="⬅️", row=2)
    async def back(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.edit_message(embed=self.parent_view.get_main_embed(), view=self.parent_view)


class AutoCleanChannelSelectMenu(ui.Select):
    def __init__(self, parent_view):
        self.parent_view = parent_view
        super().__init__(placeholder="Select channel...", min_values=1, max_values=1, row=0)

    async def callback(self, interaction: discord.Interaction):
        self.parent_view.selected_channel_id = self.values[0]
        await interaction.response.edit_message(embed=self.parent_view.get_embed(), view=self.parent_view)

    def _populate_channels(self, guild: discord.Guild):
        self.options = []
        for ch in guild.text_channels[:25]:
            self.options.append(discord.SelectOption(label=ch.name, value=str(ch.id)))


class AutoCleanDelayModal(ui.Modal, title="Configure AutoClean Delay"):
    delay = ui.TextInput(label="Deletion Delay (Seconds)", default="3600", placeholder="Seconds before delete")

    def __init__(self, cog, channel):
        super().__init__()
        self.cog = cog
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        try:
            d = int(str(self.delay))
            await self.cog.config.channel(self.channel).delay.set(d)
            await interaction.response.send_message(f"✅ Delay updated to **{d} seconds** for <#{self.channel.id}>.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Input must be a valid integer.", ephemeral=True)


# =====================================================================
#                      WELLBEING SUBSYSTEM VIEW
# =====================================================================
class WellbeingSubsystemView(ui.View):
    def __init__(self, bot, author, cog, parent_view, guild):
        super().__init__(timeout=180)
        self.bot = bot
        self.author = author
        self.cog = cog
        self.parent_view = parent_view
        self.selected_channel_id = None
        
        menu = WellbeingChannelSelectMenu(self)
        menu._populate_channels(guild)
        self.add_item(menu)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Unauthorized.", ephemeral=True)
            return False
        return True

    def get_embed(self) -> discord.Embed:
        desc = (
            f"```ansi\n"
            f"{CYAN}╔══════════════════════════════════════════════════════╗{RESET}\n"
            f"{CYAN}║            🏥 WELLBEING REMINDERS COG                 ║{RESET}\n"
            f"{CYAN}╚══════════════════════════════════════════════════════╝{RESET}\n\n"
            f" Manage terminal rules & wellbeing broadcast channels.\n"
            f" Selected Channel ID: {self.selected_channel_id or 'None'}\n"
            f"```"
        )
        return discord.Embed(title="Subsystem: Wellbeing Reminders", description=desc, color=discord.Color.cyan())

    @ui.button(label="Add Alert Channel", style=discord.ButtonStyle.primary, row=1)
    async def add_channel(self, interaction: discord.Interaction, button: ui.Button):
        if not self.selected_channel_id:
            return await interaction.response.send_message("❌ Please select a channel first.", ephemeral=True)
        cid = int(self.selected_channel_id)
        
        async with self.cog.config.channels() as channels:
            if cid in channels:
                return await interaction.response.send_message("⚠️ Channel already exists in wellbeing broadcasts.", ephemeral=True)
            channels.append(cid)
        await interaction.response.send_message(f"✅ Added <#{cid}> to wellbeing broadcast lists.", ephemeral=True)

    @ui.button(label="Remove Alert Channel", style=discord.ButtonStyle.primary, row=1)
    async def remove_channel(self, interaction: discord.Interaction, button: ui.Button):
        if not self.selected_channel_id:
            return await interaction.response.send_message("❌ Please select a channel first.", ephemeral=True)
        cid = int(self.selected_channel_id)
        
        async with self.cog.config.channels() as channels:
            if cid not in channels:
                return await interaction.response.send_message("⚠️ Channel is not in wellbeing broadcasts.", ephemeral=True)
            channels.remove(cid)
        await interaction.response.send_message(f"✅ Removed <#{cid}> from wellbeing broadcasts.", ephemeral=True)

    @ui.button(label="Main Menu", style=discord.ButtonStyle.danger, emoji="⬅️", row=2)
    async def back(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.edit_message(embed=self.parent_view.get_main_embed(), view=self.parent_view)


class WellbeingChannelSelectMenu(ui.Select):
    def __init__(self, parent_view):
        self.parent_view = parent_view
        super().__init__(placeholder="Select channel...", min_values=1, max_values=1, row=0)

    async def callback(self, interaction: discord.Interaction):
        self.parent_view.selected_channel_id = self.values[0]
        await interaction.response.edit_message(embed=self.parent_view.get_embed(), view=self.parent_view)

    def _populate_channels(self, guild: discord.Guild):
        self.options = []
        for ch in guild.text_channels[:25]:
            self.options.append(discord.SelectOption(label=ch.name, value=str(ch.id)))


# =====================================================================
#                      ECONOMY SUBSYSTEM VIEW
# =====================================================================
class EconomySubsystemView(ui.View):
    def __init__(self, bot, author, parent_view):
        super().__init__(timeout=180)
        self.bot = bot
        self.author = author
        self.parent_view = parent_view

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Unauthorized.", ephemeral=True)
            return False
        return True

    def get_embed(self) -> discord.Embed:
        desc = (
            f"```ansi\n"
            f"{GREEN}╔══════════════════════════════════════════════════════╗{RESET}\n"
            f"{GREEN}║            💰 SERVER ECONOMY & BANK SUBSYSTEM         ║{RESET}\n"
            f"{GREEN}╚══════════════════════════════════════════════════════╝{RESET}\n\n"
            f" Manage default balances, paydays, and credit pools.\n"
            f"```"
        )
        return discord.Embed(title="Subsystem: Economy & Bank", description=desc, color=discord.Color.green())

    @ui.button(label="Set Default Balance", style=discord.ButtonStyle.primary, row=0)
    async def set_default_bal(self, interaction: discord.Interaction, button: ui.Button):
        modal = EconomyDefaultBalModal()
        await interaction.response.send_modal(modal)

    @ui.button(label="Set All Balances", style=discord.ButtonStyle.primary, row=0)
    async def set_all_bal(self, interaction: discord.Interaction, button: ui.Button):
        modal = EconomySetAllModal()
        await interaction.response.send_modal(modal)

    @ui.button(label="Configure Payday", style=discord.ButtonStyle.secondary, row=1)
    async def config_payday(self, interaction: discord.Interaction, button: ui.Button):
        modal = EconomyPaydayModal()
        await interaction.response.send_modal(modal)

    @ui.button(label="Main Menu", style=discord.ButtonStyle.danger, emoji="⬅️", row=2)
    async def back(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.edit_message(embed=self.parent_view.get_main_embed(), view=self.parent_view)


class EconomyDefaultBalModal(ui.Modal, title="Set Default Starting Balance"):
    amount = ui.TextInput(label="Amount (Credits)", default="5000", placeholder="New user baseline")

    async def on_submit(self, interaction: discord.Interaction):
        try:
            amt = int(str(self.amount))
            await bank.set_default_balance(interaction.guild, amt)
            await interaction.response.send_message(f"✅ Default starting balance updated to **{amt}**.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Input must be a valid integer.", ephemeral=True)


class EconomySetAllModal(ui.Modal, title="Set All Balances (Guild-Wide)"):
    amount = ui.TextInput(label="Set Credits", default="10000", placeholder="Warning: overwrites everyone!")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            amt = int(str(self.amount))
            guild = interaction.guild
            count = 0
            for member in guild.members:
                if not member.bot:
                    try:
                        await bank.set_balance(member, amt)
                        count += 1
                    except Exception:
                        pass
            await interaction.followup.send(f"✅ Set bank balance to **{amt}** for {count} members successfully.", ephemeral=True)
        except ValueError:
            await interaction.followup.send("❌ Input must be a valid integer.", ephemeral=True)


class EconomyPaydayModal(ui.Modal, title="Configure Payday System"):
    credits = ui.TextInput(label="Credits per Payday", default="250", placeholder="E.g. 250")
    seconds = ui.TextInput(label="Cooldown (Seconds)", default="86400", placeholder="E.g. 86400 (24h)")

    async def on_submit(self, interaction: discord.Interaction):
        try:
            c = int(str(self.credits))
            s = int(str(self.seconds))
            
            # Access the built-in Economy cog's config directly
            eco_conf = Config.get_conf(None, identifier=2707284898, cog_name="Economy")
            await eco_conf.guild(interaction.guild).payday_credits.set(c)
            await eco_conf.guild(interaction.guild).payday_time.set(s)
            
            await interaction.response.send_message(
                f"✅ Payday system updated!\n"
                f"💰 Payday: **{c} credits**\n"
                f"⏱️ Cooldown: **{s} seconds**.",
                ephemeral=True
            )
        except ValueError:
            await interaction.response.send_message("❌ Inputs must be valid integers.", ephemeral=True)
