from .sysnames import SysNames

async def setup(bot):
    await bot.add_cog(SysNames(bot))
