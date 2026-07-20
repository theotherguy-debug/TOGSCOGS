from .root import Root

async def setup(bot):
    await bot.add_cog(Root(bot))
