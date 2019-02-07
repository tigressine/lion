from discord.ext import commands

def setup(bot):
    bot.add_cog(InfoCog())

class InfoCog:

    @commands.command()
    async def info_command(self, context):
        await context.send("infffooo")
