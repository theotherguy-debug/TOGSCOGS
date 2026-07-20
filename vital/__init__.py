from .vital import Vital

async def setup(bot):
    await bot.add_cog(Vital(bot))
