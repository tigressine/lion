"""An administration cog for delicate functions.

Written by Tiger Sachse.
"""
import utilities
from discord.ext import commands


def setup(bot):
    """Add this cog to a given bot."""
    bot.add_cog(AdministrationCog(bot))


class AdministrationCog(commands.Cog):
    """This class contains several delicate commands."""
    @commands.command(name="reroute", usage="!reroute")
    @commands.check(utilities.is_administrator)
    async def reroute_command(self, context):
        """Change my default communication channel."""
        context.bot.set_guild_setting(context.guild.id,
                                      "default_channel",
                                      context.message.channel.id)

        response = "**This channel is now my default communication channel.**"
        await utilities.respond(context, response)

    @reroute_command.error
    async def reroute_error(self, context, error):
        """Handle any errors that occurred during the 'reroute' command."""
        if isinstance(error, commands.errors.CheckFailure):
            message = "You must be an administrator to run this command."
            await utilities.throw_error(context, error, message)
        else:
            await utilities.throw_error(context, error)
