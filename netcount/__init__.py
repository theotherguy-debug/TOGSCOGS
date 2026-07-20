from .netcount import NetCount

async def setup(bot):
    await bot.add_cog(NetCount(bot))
