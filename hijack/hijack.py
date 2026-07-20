import asyncio
import random
import time
import discord
from redbot.core import commands, app_commands

# Try to import storage and ui helpers from original terminaloperator
try:
    from togcogs.terminaloperator.storage import TerminalStorage
    from togcogs.terminaloperator.achievements import ACHIEVEMENTS, get_rank
    from togcogs.terminaloperator.ui import make_firewall_bar, make_alert
except ImportError:
    try:
        from tobcogs.terminaloperator.storage import TerminalStorage
        from tobcogs.terminaloperator.achievements import ACHIEVEMENTS, get_rank
        from tobcogs.terminaloperator.ui import make_firewall_bar, make_alert
    except ImportError:
        try:
            from ..terminaloperator.storage import TerminalStorage
            from ..terminaloperator.achievements import ACHIEVEMENTS, get_rank
            from ..terminaloperator.ui import make_firewall_bar, make_alert
        except ImportError:
            # Standalone Fallback definitions in case cogs are imported differently
            from redbot.core import Config
            
            class TerminalStorage:
                def __init__(self):
                    self.config = Config.get_conf(
                        self,
                        identifier=982374923874,
                        force_registration=True,
                    )
                    self.config.register_user(
                        firewall=100,
                        pwns=0,
                        achievements=[],
                    )
                async def get_firewall(self, user_id):
                    return await self.config.user_from_id(user_id).firewall()
                async def set_firewall(self, user_id, value):
                    value = max(0, min(100, value))
                    await self.config.user_from_id(user_id).firewall.set(value)
                async def reset_firewall(self, user_id):
                    await self.config.user_from_id(user_id).firewall.set(100)
                async def add_pwn(self, user_id):
                    user = self.config.user_from_id(user_id)
                    current = await user.pwns()
                    new = current + 1
                    await user.pwns.set(new)
                    return new
                async def get_pwns(self, user_id):
                    return await self.config.user_from_id(user_id).pwns()
                async def get_achievements(self, user_id):
                    return await self.config.user_from_id(user_id).achievements()
                async def unlock_achievement(self, user_id, key):
                    user = self.config.user_from_id(user_id)
                    current = await user.achievements()
                    if key not in current:
                        current.append(key)
                        await user.achievements.set(current)
                        return True
                    return False
                async def get_leaderboard(self):
                    all_users = await self.config.all_users()
                    return {uid: data["pwns"] for uid, data in all_users.items()}
            
            ACHIEVEMENTS = {
                "FIRST_BLOOD": "First successful breach.",
                "FIREWALL_DESTROYER": "10 total pwns.",
                "MASTER_OPERATOR": "50 total pwns.",
            }
            
            def get_rank(pwns: int) -> str:
                if pwns >= 100: return "ROOT ACCESS"
                if pwns >= 50: return "Cyber Architect"
                if pwns >= 30: return "Network Infiltrator"
                if pwns >= 15: return "Security Analyst"
                if pwns >= 5: return "Field Technician"
                return "Novice Operator"
                
            def make_firewall_bar(percent: int) -> str:
                percent = max(0, min(100, percent))
                bar_size = 20
                filled = int((percent / 100) * bar_size)
                return "█" * filled + " " * (bar_size - filled)

            def make_alert(threat_name: str, status: str, message: str) -> str:
                header = "╔" + "═" * 69 + "╗"
                title = "║" + "CRITICAL SYSTEM ALERT".center(69) + "║"
                footer = "╚" + "═" * 69 + "╝"
                output = [
                    header, title, footer, "",
                    " [!] SYSTEM COMPROMISE DETECTED",
                    f" [!] DETECTED THREAT: {threat_name}",
                    f" [!] STATUS: {status} [⚠️ ALERT]", "",
                    f" [!] ALERT: {message}",
                    " [!] ACCESS: Internal protocols compromised.", "",
                    " 📥 EMERGENCY ACTION REQUIRED.",
                    " [████████████████████                                     ] 100%",
                ]
                return "```" + "\n".join(output) + "```"


class DecryptionModal(discord.ui.Modal, title="Decryption Console"):
    node_name = discord.ui.TextInput(
        label="Enter Node Name to Decrypt",
        placeholder="e.g. DATABASE_SRV",
        min_length=1,
        max_length=32,
        required=True
    )

    def __init__(self, cog):
        super().__init__()
        self.cog = cog

    async def on_submit(self, interaction: discord.Interaction):
        node = self.node_name.value.strip()
        await interaction.response.defer(ephemeral=True)
        await asyncio.sleep(1.5)
        success = random.choice([True, False, False])
        if success:
            key = random.randint(1000, 9999)
            await interaction.followup.send(
                f"```[SUCCESS]: Node {node} decrypted. Key: 0x{key}ABCD```",
                ephemeral=True
            )
        else:
            await interaction.followup.send(
                f"```[FAILURE]: Decryption failed for {node}.```",
                ephemeral=True
            )


class AdminView(discord.ui.View):
    def __init__(self, cog, author):
        super().__init__(timeout=60.0)
        self.cog = cog
        self.author = author

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("Only the initiating administrator can interact with this panel.", ephemeral=True)
            return False
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("You do not have permission to access administrator commands.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Trigger DDoS", style=discord.ButtonStyle.danger, emoji="🔥")
    async def ddos_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        all_users = await self.cog.storage.config.all_users()
        for uid in all_users.keys():
            hp = await self.cog.storage.get_firewall(uid)
            dmg = random.randint(10, 30)
            await self.cog.storage.set_firewall(uid, max(0, hp - dmg))
            
        await interaction.channel.send("```[EVENT]: Massive DDoS detected. All firewalls impacted.\n[EVENT COMPLETE]: Network stability compromised.```")
        await interaction.followup.send("DDoS event triggered.", ephemeral=True)

    @discord.ui.button(label="Toggle Lockdown", style=discord.ButtonStyle.danger, emoji="🔒")
    async def lockdown_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        original_cog = self.cog.bot.get_cog("TerminalOperator")
        if original_cog and hasattr(original_cog, "events"):
            current = original_cog.events.lockdown_active
            original_cog.events.lockdown_active = not current
            new_state = original_cog.events.lockdown_active
        else:
            self.cog.lockdown_active = not self.cog.lockdown_active
            new_state = self.cog.lockdown_active
            
        status = "ENABLED (Breach protocols offline)" if new_state else "DISABLED (Breach protocols active)"
        await interaction.channel.send(f"```[LOCKDOWN]: Security lockdown status is now: {status}.```")
        await interaction.response.send_message(f"Lockdown status toggled to {new_state}.", ephemeral=True)

    @discord.ui.button(label="Trigger Purge", style=discord.ButtonStyle.danger, emoji="🧹")
    async def purge_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        all_users = await self.cog.storage.config.all_users()
        for uid in all_users.keys():
            await self.cog.storage.set_firewall(uid, 1)
            
        await interaction.channel.send("```[PURGE]: System purge initiated. All firewalls reduced to 1%.\n[PURGE COMPLETE]: Next breach guarantees pwn.```")
        await interaction.followup.send("System purge triggered.", ephemeral=True)


class MainTerminalView(discord.ui.View):
    def __init__(self, cog, author):
        super().__init__(timeout=60.0)
        self.cog = cog
        self.author = author
        self.message = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "This terminal console is locked to the operator who initialized it.", 
                ephemeral=True
            )
            return False
        return True

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        try:
            if self.message:
                embed = self.message.embeds[0]
                embed.title = "❌ SECURE HUD TERMINAL (SESSION TIMED OUT)"
                embed.color = discord.Color.dark_grey()
                await self.message.edit(embed=embed, view=self)
        except Exception:
            pass

    @discord.ui.button(label="Status", style=discord.ButtonStyle.primary, emoji="📊", row=0)
    async def status_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        storage = self.cog.storage
        hp = await storage.get_firewall(self.author.id)
        pwns = await storage.get_pwns(self.author.id)
        achievements = await storage.get_achievements(self.author.id)
        rank = get_rank(pwns)
        
        ach_text = ", ".join(achievements) if achievements else "None"
        bar = make_firewall_bar(hp)
        
        embed = discord.Embed(title="💾 OPERATOR STATUS REPORT", color=discord.Color.dark_green())
        embed.add_field(name="Operator", value=self.author.display_name, inline=True)
        embed.add_field(name="Rank", value=rank, inline=True)
        embed.add_field(name="PWNs", value=str(pwns), inline=True)
        embed.add_field(name="Firewall Integrity", value=f"{hp}% [{bar}]", inline=False)
        embed.add_field(name="Achievements Unlocked", value=ach_text, inline=False)
        embed.set_footer(text="System online. Keep firewalls reinforced.")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Scan Network", style=discord.ButtonStyle.primary, emoji="📡", row=0)
    async def scan_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        nodes = ["DATABASE_SRV", "MAIL_RELAY", "SEC_FIREWALL", "CORE_CPU", "USER_ENDPOINT"]
        node = random.choice(nodes)
        integrity = random.randint(40, 99)
        
        await asyncio.sleep(1.0)
        await interaction.followup.send(
            f"```[SCAN]: Node {node} responding on Port 8080. Integrity: {integrity}%```",
            ephemeral=True
        )

    @discord.ui.button(label="Decrypt Node", style=discord.ButtonStyle.primary, emoji="🔑", row=0)
    async def decrypt_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(DecryptionModal(self.cog))

    @discord.ui.button(label="Self-Repair", style=discord.ButtonStyle.success, emoji="🛠️", row=1)
    async def repair_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.storage.reset_firewall(self.author.id)
        await interaction.response.send_message("```[LOG]: Firewall cluster restored to 100%.```", ephemeral=True)

    @discord.ui.button(label="Leaderboard", style=discord.ButtonStyle.secondary, emoji="🏆", row=1)
    async def leaderboard_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        storage = self.cog.storage
        lb = await storage.get_leaderboard()
        if not lb:
            await interaction.response.send_message("```[LOG]: No breaches recorded.```", ephemeral=True)
            return

        sorted_lb = sorted(lb.items(), key=lambda x: (-x[1], x[0]))[:5]
        text = "╔══════════ TOP OPERATORS ══════════╗\n"

        for i, (uid, count) in enumerate(sorted_lb, 1):
            try:
                user = await self.cog.bot.fetch_user(uid)
                name = user.name
            except Exception:
                name = f"User_{uid}"
            text += f"║ {i}. {name.ljust(20)} | {count} PWNS ║\n"

        text += "╚═══════════════════════════════════╝"
        await interaction.response.send_message(f"```md\n{text}\n```", ephemeral=True)

    @discord.ui.button(label="Manual", style=discord.ButtonStyle.secondary, emoji="📖", row=1)
    async def manual_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        manual = (
            "╔══════════════ OPERATOR MANUAL ══════════════╗\n"
            "║ /terminalui      : Open this interactive HUD ║\n"
            "║ /breachui <user> : Attack target (UI battle)   ║\n"
            "║ /statsui [user]  : Inspect operator stats      ║\n"
            "║ /scanui          : Run port check command     ║\n"
            "║ /leaderboardui   : Print operator rankings    ║\n"
            "║ /repairui <user> : Restore user firewall       ║\n"
            "╚══════════════════════════════════════════════╝"
        )
        await interaction.response.send_message(f"```md\n{manual}\n```", ephemeral=True)

    @discord.ui.button(label="Admin Menu", style=discord.ButtonStyle.danger, emoji="⚙️", row=1)
    async def admin_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("Only administrators can access the events dashboard.", ephemeral=True)
            return
        view = AdminView(self.cog, self.author)
        await interaction.response.send_message("`[SECURE CONNECTION]: Administrator Console initialized.`", view=view, ephemeral=True)


class BreachView(discord.ui.View):
    def __init__(self, cog, attacker, target, attacker_fw, target_fw):
        super().__init__(timeout=120.0)
        self.cog = cog
        self.attacker = attacker
        self.target = target
        self.attacker_firewall = attacker_fw
        self.target_firewall = target_fw
        self.connected = False
        self.message = None
        
        self.attacker_cooldown = 0.0
        self.target_cooldown = 0.0
        
        # Configure initial button states
        self.inject_payload.disabled = True
        self.bypass_firewall.disabled = True
        self.reinforce.disabled = True
        self.counter_trace.disabled = True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id not in [self.attacker.id, self.target.id]:
            await interaction.response.send_message(
                "You are not part of this active cyber-warfare session.", 
                ephemeral=True
            )
            return False
            
        now = time.time()
        if interaction.user.id == self.attacker.id:
            if now - self.attacker_cooldown < 1.5:
                await interaction.response.send_message("⚠️ Your terminal is cooling down. Please wait 1.5 seconds.", ephemeral=True)
                return False
        elif interaction.user.id == self.target.id:
            if not self.connected:
                await interaction.response.send_message("❌ Cannot perform defensive measures before the attacker establishes a connection.", ephemeral=True)
                return False
            if now - self.target_cooldown < 1.5:
                await interaction.response.send_message("⚠️ Your defensive node is cooling down. Please wait 1.5 seconds.", ephemeral=True)
                return False
        return True

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        try:
            if self.message:
                embed = self.message.embeds[0]
                embed.title = "❌ BREACH TERMINAL (SESSION TIMED OUT)"
                embed.color = discord.Color.red()
                await self.message.edit(
                    content=f"`[DISCONNECTED]: Session targeting {self.target.display_name} timed out.`", 
                    embed=embed, 
                    view=self
                )
        except Exception:
            pass

    async def update_embed(self, extra_log: str = "") -> discord.Embed:
        bar_target = make_firewall_bar(self.target_firewall)
        bar_attacker = make_firewall_bar(self.attacker_firewall)
        
        embed = discord.Embed(
            title="⚔️ REAL-TIME PVP CYBER WARFARE",
            color=discord.Color.red() if self.connected else discord.Color.dark_grey()
        )
        embed.add_field(name="🔺 Hacker (Attacker)", value=f"{self.attacker.display_name}\n💻 Firewall: {self.attacker_firewall}%\n[{bar_attacker}]", inline=False)
        embed.add_field(name="🛡️ Target (Defender)", value=f"{self.target.display_name}\n💻 Firewall: {self.target_firewall}%\n[{bar_target}]", inline=False)
        
        status_text = "🔴 CONNECTION ESTABLISHED - BATTLE ACTIVE" if self.connected else "⚪ OFFLINE (WAITING FOR HACKER CONNECT)"
        embed.add_field(name="Link Status", value=status_text, inline=True)
        
        if extra_log:
            embed.add_field(name="System Console Log", value=f"```\n{extra_log}\n```", inline=False)
            
        return embed

    @discord.ui.button(label="Connect", style=discord.ButtonStyle.primary, emoji="🔌", row=0)
    async def connect_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.attacker_cooldown = time.time()
        self.connected = True
        button.disabled = True
        
        self.inject_payload.disabled = False
        self.bypass_firewall.disabled = False
        self.reinforce.disabled = False
        self.counter_trace.disabled = False
        
        embed = await self.update_embed(
            "[BREACH]: Establishing connection...\n"
            "[BREACH]: Injecting payload...\n"
            "[BREACH]: Link established! Defenses and counters unlocked!"
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Inject Payload", style=discord.ButtonStyle.danger, emoji="⚔️", row=0)
    async def inject_payload(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.attacker_cooldown = time.time()
        
        dmg = random.randint(15, 25)
        self.target_firewall = max(0, self.target_firewall - dmg)
        await self.cog.storage.set_firewall(self.target.id, self.target_firewall)
        
        log = f"[ATTACK]: {self.attacker.display_name} injected payload! Damage: {dmg}%"
        await self.check_game_over(interaction, log)

    @discord.ui.button(label="Bypass", style=discord.ButtonStyle.success, emoji="📡", row=0)
    async def bypass_firewall(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.attacker_cooldown = time.time()
        
        success = random.choice([True, False])
        if success:
            dmg = random.randint(30, 50)
            self.target_firewall = max(0, self.target_firewall - dmg)
            log = f"[BYPASS SUCCESS]: Attacker breached firewall gates! Damage: {dmg}%"
            await self.cog.storage.set_firewall(self.target.id, self.target_firewall)
        else:
            backfire = random.randint(15, 25)
            self.attacker_firewall = max(0, self.attacker_firewall - backfire)
            log = f"[BYPASS FAILURE]: Security feed looped back! Backfire damage to hacker: {backfire}%"
            await self.cog.storage.set_firewall(self.attacker.id, self.attacker_firewall)
            
        await self.check_game_over(interaction, log)

    @discord.ui.button(label="Reinforce", style=discord.ButtonStyle.success, emoji="🛡️", row=1)
    async def reinforce(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.target_cooldown = time.time()
        
        heal = random.randint(10, 25)
        self.target_firewall = min(100, self.target_firewall + heal)
        log = f"[DEFENSE]: {self.target.display_name} reinforced firewall! Restored: {heal}%"
        
        await self.cog.storage.set_firewall(self.target.id, self.target_firewall)
        await self.check_game_over(interaction, log)

    @discord.ui.button(label="Counter-Trace", style=discord.ButtonStyle.primary, emoji="🛰️", row=1)
    async def counter_trace(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.target_cooldown = time.time()
        
        dmg = random.randint(15, 25)
        self.attacker_firewall = max(0, self.attacker_firewall - dmg)
        log = f"[COUNTER]: {self.target.display_name} traced source! Hacker damage: {dmg}%"
        
        await self.cog.storage.set_firewall(self.attacker.id, self.attacker_firewall)
        await self.check_game_over(interaction, log)

    @discord.ui.button(label="Abort", style=discord.ButtonStyle.secondary, emoji="❌", row=0)
    async def abort_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
        log = "[ABORT]: Connection terminated by attacker."
        embed = await self.update_embed(log)
        embed.title = "❌ BREACH TERMINAL - SESSION ABORTED"
        embed.color = discord.Color.dark_red()
        await interaction.response.edit_message(content=f"`[SESSION TERMINATED]: {self.attacker.display_name} aborted.`", embed=embed, view=self)
        self.stop()

    async def check_game_over(self, interaction: discord.Interaction, current_log: str):
        from redbot.core import bank
        guild = interaction.guild
        currency_name = "credits"
        try:
            currency_name = await bank.get_currency_name(guild)
        except Exception:
            pass

        if self.target_firewall <= 0:
            for item in self.children:
                item.disabled = True
            
            await self.cog.storage.reset_firewall(self.target.id)
            pwns = await self.cog.storage.add_pwn(self.attacker.id)
            rank = get_rank(pwns)
            
            log = current_log + f"\n\n[!!!] SYSTEM OVERRIDE: {self.target.display_name} has been PWNED by {self.attacker.display_name}!"
            log += f"\n[RANKUP]: {self.attacker.display_name} is now a {rank}."
            
            # Transfer credits (10% steal)
            try:
                target_bal = await bank.get_balance(self.target)
                steal_amount = int(target_bal * 0.10)
                if steal_amount < 50:
                    steal_amount = min(target_bal, 50)
                if steal_amount > 0:
                    await bank.withdraw_credits(self.target, steal_amount)
                    await bank.deposit_credits(self.attacker, steal_amount)
                    log += f"\n[ECO]: Deducted {steal_amount} {currency_name} from target bank."
                else:
                    await bank.deposit_credits(self.attacker, 50)
                    log += f"\n[ECO]: Harvested 50 {currency_name} bounty from network."
            except Exception:
                pass

            ach_unlocked = []
            if pwns == 1:
                if await self.cog.storage.unlock_achievement(self.attacker.id, "FIRST_BLOOD"):
                    ach_unlocked.append("FIRST_BLOOD")
            if pwns == 10:
                if await self.cog.storage.unlock_achievement(self.attacker.id, "FIREWALL_DESTROYER"):
                    ach_unlocked.append("FIREWALL_DESTROYER")
            if pwns == 50:
                if await self.cog.storage.unlock_achievement(self.attacker.id, "MASTER_OPERATOR"):
                    ach_unlocked.append("MASTER_OPERATOR")
            if ach_unlocked:
                log += f"\n[ACHIEVEMENT UNLOCKED]: {', '.join(ach_unlocked)}"
                
            embed = await self.update_embed(log)
            embed.title = "🏆 BREACH SUCCESSFUL - TARGET OVERRIDDEN"
            embed.color = discord.Color.gold()
            await interaction.response.edit_message(
                content=f"🏆 {self.attacker.mention} successfully breached {self.target.mention}! 🏆", 
                embed=embed, 
                view=self
            )
            self.stop()
            
        elif self.attacker_firewall <= 0:
            for item in self.children:
                item.disabled = True
                
            await self.cog.storage.reset_firewall(self.attacker.id)
            pwns = await self.cog.storage.add_pwn(self.target.id)
            rank = get_rank(pwns)
            
            log = current_log + f"\n\n[🛡️ SYSTEM SECURED]: {self.attacker.display_name} was counter-traced and PWNED by {self.target.display_name}!"
            log += f"\n[RANKUP]: {self.target.display_name} is now a {rank}."
            
            # Transfer credits (10% steal)
            try:
                attacker_bal = await bank.get_balance(self.attacker)
                steal_amount = int(attacker_bal * 0.10)
                if steal_amount < 50:
                    steal_amount = min(attacker_bal, 50)
                if steal_amount > 0:
                    await bank.withdraw_credits(self.attacker, steal_amount)
                    await bank.deposit_credits(self.target, steal_amount)
                    log += f"\n[ECO]: Hijacked {steal_amount} {currency_name} from attacker's trace."
                else:
                    await bank.deposit_credits(self.target, 50)
                    log += f"\n[ECO]: Secured 50 {currency_name} defender bounty."
            except Exception:
                pass

            ach_unlocked = []
            if pwns == 1:
                if await self.cog.storage.unlock_achievement(self.target.id, "FIRST_BLOOD"):
                    ach_unlocked.append("FIRST_BLOOD")
            if pwns == 10:
                if await self.cog.storage.unlock_achievement(self.target.id, "FIREWALL_DESTROYER"):
                    ach_unlocked.append("FIREWALL_DESTROYER")
            if pwns == 50:
                if await self.cog.storage.unlock_achievement(self.target.id, "MASTER_OPERATOR"):
                    ach_unlocked.append("MASTER_OPERATOR")
            if ach_unlocked:
                log += f"\n[ACHIEVEMENT UNLOCKED]: {', '.join(ach_unlocked)}"
                
            embed = await self.update_embed(log)
            embed.title = "🛡️ DEFENSE SUCCESSFUL - ATTACKER PWNED"
            embed.color = discord.Color.blue()
            await interaction.response.edit_message(
                content=f"🛡️ {self.target.mention} successfully counter-hacked and pwned {self.attacker.mention}! 🛡️", 
                embed=embed, 
                view=self
            )
            self.stop()
            
        else:
            embed = await self.update_embed(current_log)
            await interaction.response.edit_message(embed=embed, view=self)


class Hijack(commands.Cog):
    """Modular Terminal Operator Cog with Button-based UI"""

    def __init__(self, bot):
        self.bot = bot
        self.storage = TerminalStorage()
        self.lockdown_active = False

    # ---------- Status Dashboard Command ----------
    @commands.hybrid_command(name="terminalui")
    async def terminal_ui(self, ctx):
        """Open the interactive Terminal Operator Dashboard HUD.

        Provides a graphical dashboard using buttons to check stats, run scans,
        decrypt nodes, restore health, or broadcast emergency alerts.
        """
        view = MainTerminalView(self, ctx.author)
        embed = discord.Embed(
            title="🖥️ SECURE HUD TERMINAL v2.0",
            description="Welcome to the secure operator console. Select an action below to probe the network state.",
            color=discord.Color.dark_green()
        )
        embed.add_field(name="Authorized Operator", value=ctx.author.mention, inline=True)
        embed.add_field(name="Console State", value="🟢 ONLINE / SECURE", inline=True)
        message = await ctx.send(embed=embed, view=view)
        view.message = message

    # ---------- Breach Command ----------
    @commands.hybrid_command(name="breachui")
    @app_commands.describe(target="The target operator whose firewall you want to breach.")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def breach_ui(self, ctx, target: discord.Member):
        """Attack another operator's firewall using the interactive UI console.

        Forces a connection to the target operator's system, allowing you to
        inject dangerous payloads or execute firewall bypass sequences.
        """
        attacker = ctx.author

        if target.bot:
            await ctx.send("```[ERROR]: Cannot breach bots.```")
            ctx.command.reset_cooldown(ctx)
            return
        if target.id == attacker.id:
            await ctx.send("```[ERROR]: Self-breach blocked.```")
            ctx.command.reset_cooldown(ctx)
            return
            
        # Check lockdown dynamically from the original cog or local state
        lockdown_active = self.lockdown_active
        original_cog = self.bot.get_cog("TerminalOperator")
        if original_cog and hasattr(original_cog, "events"):
            lockdown_active = original_cog.events.lockdown_active or lockdown_active
            
        if lockdown_active:
            await ctx.send("```[LOCKDOWN]: Breach disabled.```")
            ctx.command.reset_cooldown(ctx)
            return

        # Fetch both players' database firewall percentages
        attacker_fw = await self.storage.get_firewall(attacker.id)
        target_fw = await self.storage.get_firewall(target.id)

        view = BreachView(self, attacker, target, attacker_fw, target_fw)
        embed = await view.update_embed("INITIALIZING BREACH CONSOLE...\nWaiting for operator connection...")
        
        # Mention/tag target user to notify them so they can counteract
        content = f"⚠️ {target.mention} - terminal breach attempt detected from {attacker.mention}! ⚠️"
        
        message = await ctx.send(content=content, embed=embed, view=view)
        view.message = message

    # ---------- Stats Slash Command ----------
    @commands.hybrid_command(name="statsui")
    @app_commands.describe(target="The operator whose statistics you want to view.")
    async def stats_ui(self, ctx, target: discord.Member = None):
        """Inspect the terminal statistics, rank, and achievements of another operator.

        Provides a full detail check on firewall levels, ranks, and unlocked badges.
        """
        target = target or ctx.author
        storage = self.storage
        hp = await storage.get_firewall(target.id)
        pwns = await storage.get_pwns(target.id)
        achievements = await storage.get_achievements(target.id)
        rank = get_rank(pwns)
        
        ach_text = ", ".join(achievements) if achievements else "None"
        bar = make_firewall_bar(hp)
        
        embed = discord.Embed(title=f"💾 OPERATOR REPORT: {target.display_name.upper()}", color=discord.Color.dark_green())
        embed.add_field(name="Operator", value=target.mention, inline=True)
        embed.add_field(name="Rank", value=rank, inline=True)
        embed.add_field(name="PWNs", value=str(pwns), inline=True)
        embed.add_field(name="Firewall Integrity", value=f"{hp}% [{bar}]", inline=False)
        embed.add_field(name="Achievements Unlocked", value=ach_text, inline=False)
        await ctx.send(embed=embed)

    # ---------- Scan Slash Command ----------
    @commands.hybrid_command(name="scanui")
    async def scan_ui(self, ctx):
        """Scan the network for active ports and vulnerable nodes.

        Runs a network sweep outputting a random server node and its integrity.
        """
        nodes = ["DATABASE_SRV", "MAIL_RELAY", "SEC_FIREWALL", "CORE_CPU", "USER_ENDPOINT"]
        node = random.choice(nodes)
        integrity = random.randint(40, 99)
        async with ctx.typing():
            await asyncio.sleep(1.2)
        await ctx.send(f"```[SCAN]: Node {node} responding on Port 8080. Integrity: {integrity}%```")

    # ---------- Leaderboard Slash Command ----------
    @commands.hybrid_command(name="leaderboardui")
    async def leaderboard_ui(self, ctx):
        """Display the top operators global rankings leaderboard.

        Outputs the top 5 players sorted by most system pwns.
        """
        storage = self.storage
        lb = await storage.get_leaderboard()
        if not lb:
            await ctx.send("```[LOG]: No breaches recorded.```")
            return

        sorted_lb = sorted(lb.items(), key=lambda x: (-x[1], x[0]))[:5]
        text = "╔══════════ TOP OPERATORS ══════════╗\n"

        for i, (uid, count) in enumerate(sorted_lb, 1):
            try:
                user = await self.bot.fetch_user(uid)
                name = user.name
            except Exception:
                name = f"User_{uid}"
            text += f"║ {i}. {name.ljust(20)} | {count} PWNS ║\n"

        text += "╚═══════════════════════════════════╝"
        await ctx.send(f"```md\n{text}\n```")

    # ---------- Firewall Repair Command ----------
    @commands.hybrid_command(name="repairui")
    @app_commands.describe(target="The operator whose firewall you want to repair. Defaults to yourself.")
    async def repair_ui(self, ctx, target: discord.Member = None):
        """Restore the firewall cluster integrity of an operator.

        Sets the target's firewall back to 100% stable condition.
        """
        target = target or ctx.author
        await self.storage.reset_firewall(target.id)
        await ctx.send(f"```[LOG]: Firewall restored for {target.display_name}.```")
