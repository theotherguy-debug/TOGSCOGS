import asyncio
import datetime
import discord
from redbot.core import commands, Config


class Purge(commands.Cog):
    """Safely cleans up messages in real-time or via scheduled sweeps."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=98473625112,
            force_registration=True,
        )

        default_channel = {
            "enabled": False,         # Live delay deletion active
            "delay": 3600,             # Delay in seconds for live deletion
            "sweep_enabled": False,   # Background periodic sweeping active
            "sweep_days": 5,           # Age in days for periodic sweeps
            "keep_pinned": True,       # Preserve pinned messages
            "ignored_users": [],
            "ignored_roles": [],
        }
        self.config.register_channel(**default_channel)

        default_global = {
            "log_channels": []
        }
        self.config.register_global(**default_global)

        self._tracked_tasks = set()
        self.bg_loop = self.bot.loop.create_task(self.maintenance_sweep_loop())
        self.monthly_loop = self.bot.loop.create_task(self.monthly_channel_purge_loop())

    def cog_unload(self):
        # Cancel live deletion tasks
        for task in list(self._tracked_tasks):
            task.cancel()
        # Cancel background loops
        self.bg_loop.cancel()
        self.monthly_loop.cancel()

    def _spawn_managed_task(self, coro):
        task = asyncio.create_task(coro)
        self._tracked_tasks.add(task)
        task.add_done_callback(self._tracked_tasks.discard)
        return task

    async def _delete_msg(self, message: discord.Message, delay: int):
        try:
            await asyncio.sleep(delay)
            # Fetch fresh state of the message to check if it was pinned after sending
            try:
                msg = await message.channel.fetch_message(message.id)
                keep_pinned = await self.config.channel(message.channel).keep_pinned()
                if keep_pinned and msg.pinned:
                    return
            except discord.NotFound:
                return
            except discord.HTTPException:
                pass

            await message.delete()

        except asyncio.CancelledError:
            pass
        except (discord.HTTPException, discord.Forbidden):
            pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild or message.author.bot:
            return

        config = await self.config.channel(message.channel).all()
        if not config["enabled"]:
            return

        if message.author.id in config["ignored_users"]:
            return

        if any(role.id in config["ignored_roles"] for role in message.author.roles):
            return

        self._spawn_managed_task(self._delete_msg(message, config["delay"]))

    async def maintenance_sweep_loop(self):
        """Background loop scanning channels every hour for older messages."""
        await self.bot.wait_until_ready()
        try:
            while True:
                await asyncio.sleep(3600)
                all_channels_data = await self.config.all_channels()

                for channel_id, settings in all_channels_data.items():
                    if not settings.get("sweep_enabled"):
                        continue

                    channel = self.bot.get_channel(channel_id)
                    if not channel:
                        continue

                    sweep_days = settings.get("sweep_days", 5)
                    cutoff_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=sweep_days)

                    try:
                        async for message in channel.history(limit=500, before=cutoff_time, oldest_first=True):
                            if settings.get("keep_pinned", True) and message.pinned:
                                continue
                            if message.author.id in settings.get("ignored_users", []):
                                continue
                            if any(role.id in settings.get("ignored_roles", []) for role in message.author.roles):
                                continue

                            try:
                                await message.delete()
                                await asyncio.sleep(0.5)
                            except discord.HTTPException:
                                pass
                    except discord.Forbidden:
                        pass
        except asyncio.CancelledError:
            pass

    async def monthly_channel_purge_loop(self):
        """Automated cleaner wiping designated log channels every 30 days."""
        await self.bot.wait_until_ready()
        try:
            while True:
                await asyncio.sleep(30 * 86400)
                log_channels = await self.config.log_channels()
                for channel_id in log_channels:
                    channel = self.bot.get_channel(channel_id)
                    if not channel:
                        continue
                    try:
                        await channel.purge(limit=5000)
                    except discord.HTTPException:
                        pass
        except asyncio.CancelledError:
            pass

    # --- MANAGEMENT COMMAND GROUP ---

    @commands.group(aliases=["cleaner"])
    @commands.admin_or_permissions(manage_messages=True)
    async def autoclean(self, ctx):
        """Manage auto-cleaning parameters for text channels."""
        pass

    @autoclean.command()
    async def toggle(self, ctx):
        """Toggle real-time delay deletion for this channel."""
        current = await self.config.channel(ctx.channel).enabled()
        await self.config.channel(ctx.channel).enabled.set(not current)
        status = "🟢 ACTIVE (Live Delay Deletion)" if not current else "🔴 DISABLED"
        await ctx.send(f"Auto-clean live deletion is now **{status}** for {ctx.channel.mention}.")

    @autoclean.command()
    async def delay(self, ctx, seconds: int):
        """Set the live deletion delay in seconds (minimum: 5 seconds)."""
        if seconds < 5:
            return await ctx.send("⚠️ Delay must be at least 5 seconds.")
        await self.config.channel(ctx.channel).delay.set(seconds)
        await ctx.send(f"⏱️ Messages will expire after **{seconds} seconds**.")

    @autoclean.command()
    async def sweep(self, ctx):
        """Toggle scheduled sweeps for older messages in this channel."""
        current = await self.config.channel(ctx.channel).sweep_enabled()
        await self.config.channel(ctx.channel).sweep_enabled.set(not current)
        days = await self.config.channel(ctx.channel).sweep_days()
        status = f"🟢 ACTIVE (Sweeping messages older than {days} days)" if not current else "🔴 DISABLED"
        await ctx.send(f"Auto-clean periodic sweeping is now **{status}** for {ctx.channel.mention}.")

    @autoclean.command()
    async def sweepdays(self, ctx, days: int):
        """Set how many days old messages must be before being swept (minimum: 1 day)."""
        if days < 1:
            return await ctx.send("⚠️ Sweep age must be at least 1 day.")
        await self.config.channel(ctx.channel).sweep_days.set(days)
        await ctx.send(f"🧹 Periodic sweeps will delete messages older than **{days} days**.")

    @autoclean.command()
    async def pinmode(self, ctx):
        """Toggle whether pinned messages should be preserved."""
        current = await self.config.channel(ctx.channel).keep_pinned()
        await self.config.channel(ctx.channel).keep_pinned.set(not current)
        status = "🛡️ PRESERVED" if not current else "🗑️ PURGED"
        await ctx.send(f"Pinned messages in this channel are now **{status}**.")

    @autoclean.command()
    async def ignoreuser(self, ctx, user: discord.Member):
        """Add or remove a user from the cleanup whitelist."""
        async with self.config.channel(ctx.channel).ignored_users() as users:
            if user.id in users:
                users.remove(user.id)
                await ctx.send(f"🛑 User {user.mention} removed from whitelist.")
            else:
                users.append(user.id)
                await ctx.send(f"🛡️ User {user.mention} added to whitelist.")

    @autoclean.command()
    async def ignorerole(self, ctx, role: discord.Role):
        """Add or remove a role from the cleanup whitelist."""
        async with self.config.channel(ctx.channel).ignored_roles() as roles:
            if role.id in roles:
                roles.remove(role.id)
                await ctx.send(f"🛑 Role **{role.name}** removed from whitelist.")
            else:
                roles.append(role.id)
                await ctx.send(f"🛡️ Role **{role.name}** added to whitelist.")

    @autoclean.command()
    async def clearnow(self, ctx, amount: int = 100):
        """Instantly purge up to 2000 messages in the current channel."""
        if not 1 <= amount <= 2000:
            return await ctx.send("⚠️ Choose a value between 1 and 2000.")

        status = await ctx.send(f"🧹 Purging up to `{amount}` messages...")
        try:
            deleted = await ctx.channel.purge(
                limit=amount + 1,
                check=lambda m: m.id != status.id,
            )
            await status.edit(content=f"✅ Deleted `{len(deleted)}` messages.")
            self._spawn_managed_task(self._delete_msg(status, 5))
        except discord.HTTPException:
            await ctx.send("⚠️ I couldn't clear messages. Check my channel permissions.")

    @autoclean.command()
    async def addlogchannel(self, ctx):
        """Register current channel to be wiped completely once a month."""
        async with self.config.log_channels() as channels:
            if ctx.channel.id in channels:
                return await ctx.send("⚠️ Already registered for monthly wipes.")
            channels.append(ctx.channel.id)
        await ctx.send(f"🧹 Registered {ctx.channel.mention}! Wiping every 30 days.")

    @autoclean.command()
    async def removelogchannel(self, ctx):
        """Remove current channel from the monthly wipe list."""
        async with self.config.log_channels() as channels:
            if ctx.channel.id not in channels:
                return await ctx.send("⚠️ This channel is not registered for monthly wipes.")
            channels.remove(ctx.channel.id)
        await ctx.send(f"🛑 Removed {ctx.channel.mention} from monthly wipe list.")

    @autoclean.command()
    async def listlogs(self, ctx):
        """List all channels registered for monthly sweeps."""
        log_channels = await self.config.log_channels()
        if not log_channels:
            return await ctx.send("⚠️ No channels registered for monthly log sweeps.")
        mentions = [
            self.bot.get_channel(cid).mention if self.bot.get_channel(cid) else f"`Unknown Channel ({cid})`"
            for cid in log_channels
        ]
        await ctx.send("**Channels queued for 30-day automated wipes:**\n" + "\n".join(f"• {m}" for m in mentions))

    @autoclean.command()
    async def clearlogs(self, ctx):
        """Force immediate purge of all registered monthly wipe channels."""
        log_channels = await self.config.log_channels()
        if not log_channels:
            return await ctx.send("⚠️ No log channels registered.")

        status_msg = await ctx.send("🧹 Wiping all registered monthly sweep channels...")
        purged = 0
        for cid in log_channels:
            channel = self.bot.get_channel(cid)
            if not channel:
                continue
            try:
                await channel.purge(limit=5000)
                purged += 1
            except discord.HTTPException:
                pass
        await status_msg.edit(content=f"✅ Cleared `{purged}` log channels.")

    @autoclean.command()
    async def status(self, ctx):
        """Display the complete cleanup status for this channel."""
        config = await self.config.channel(ctx.channel).all()
        log_channels = await self.config.log_channels()
        is_log_channel = ctx.channel.id in log_channels

        msg = (
            f"📊 **AutoClean Configuration Status**\n"
            f"• **Live Delay Deletion**: `{'🟢 ENABLED' if config['enabled'] else '🔴 DISABLED'}`\n"
            f"  - Deletion Delay: `{config['delay']} seconds`\n"
            f"• **Periodic Sweep Clean**: `{'🟢 ENABLED' if config['sweep_enabled'] else '🔴 DISABLED'}`\n"
            f"  - Sweep Age threshold: `{config['sweep_days']} days`\n"
            f"• **Monthly Wipe Queue**: `{'🟢 IN QUEUE' if is_log_channel else '🔴 NOT IN QUEUE'}`\n"
            f"• **Settings Whitelist & Safety**:\n"
            f"  - Preserve Pinned: `{config['keep_pinned']}`\n"
            f"  - Ignored Users: `{len(config['ignored_users'])}`\n"
            f"  - Ignored Roles: `{len(config['ignored_roles'])}`"
        )
        await ctx.send(msg)
