"""
Written by Tiger Sachse.
"""
import utilities
from discord.ext import commands


def setup(bot):
    """Add this cog to a given bot."""
    bot.add_cog(AdministrationCog())


class AdministrationCog:
    """"""
    @commands.command(name="admin")
    @commands.check(utilities.is_administrator)
    async def admin_command(self, context, flag):
        """"""
        if flag == "--default-channel":
            context.bot.set_guild_setting(context.guild.id,
                                          "default_channel",
                                          context.message.channel.id)

            response = "**This channel is now the default bot communication channel.**"
            await utilities.respond(context, response)
        else:
            raise commands.errors.BadArgument("Flag not available.")

    @admin_command.error
    async def admin_error(self, context, error):
        """"""
        if isinstance(error, commands.errors.CheckFailure):
            message = "You must be an administrator to run this command."
            await utilities.throw_error(context, error, message)
        else:
            await utilities.throw_error(context, error)
