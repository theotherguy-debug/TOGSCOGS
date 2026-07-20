from .hijack import Hijack

async def setup(bot):
    await bot.add_cog(Hijack(bot))
