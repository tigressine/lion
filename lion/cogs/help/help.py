from discord.ext import commands

def setup(bot):
    bot.add_cog(HelpCog())

class HelpCog:

    @commands.command(name="help")
    async def help_command(self, context):
        context.send("hello")
