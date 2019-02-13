""""""
import discord
import utilities
from discord.ext import commands


def setup(bot):
    """"""
    bot.add_cog(HelpCog())


class HelpCog:
    """"""
    EMBEDDED_COLOR = 0xFFEE05

    @commands.command(name="help", usage="!help")
    async def help_command(self, context):
        """Display a help menu."""
        response = "I'm Lion! Here's a list of commands I understand."
        embedded_message = discord.Embed(color=self.EMBEDDED_COLOR)

        for command in context.bot.all_commands.values():
            embedded_message.add_field(name=command.usage,
                                       value=command.help.split("\n")[0],
                                       inline=False)

        await utilities.respond(response, embed=embedded_message)

    @help_command.error
    async def help_error(self, context, error):
        """"""
        await utilities.throw_error(context, error)
