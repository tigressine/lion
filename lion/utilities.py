"""A collection of utility functions for Lion.

Written by Tiger Sachse.
"""
import time
import logging
from discord.ext import commands


async def throw_error(context,
                      error,
                      message=None,
                      delete_original=True,
                      ignore_formatting=False,
                      in_default_channel=True,
                      **keyword_arguments):
    """Send an error to the context's server.

    If a message is provided, that message is included in the post, otherwise
    the error's default message is included.
    """
    ERROR_FORMAT = ("Something went wrong!\n```\n"
                    "Command : {0}\n"
                    "Error   : {1}\n"
                    "Message : {2}\n```")

    response = ERROR_FORMAT.format(context.command,
                                   type(error).__name__,
                                   message if message is not None else error)

    context.bot.log(response, level=logging.ERROR)
    await respond(context,
                  response,
                  delete_original,
                  ignore_formatting,
                  in_default_channel,
                  **keyword_arguments)


async def respond(context,
                  message,
                  delete_original=True,
                  ignore_formatting=False,
                  in_default_channel=True,
                  **keyword_arguments):
    """Respond to a message in context.
    
    The response is automatically formatted with the original message's author's
    handle, although this can be disabled with the ignore_formatting flag.
    """
    RESPONSE_FORMAT = "{0}:\n{1}"

    # Avoid additionally formatting, if requested.
    if ignore_formatting:
        response = message
    else:
        response = RESPONSE_FORMAT.format(context.author.mention, message)

    # If requested, attempt to send the response on the default channel for the
    # user's guild.
    if in_default_channel:
        guild_settings = context.bot.get_guild_settings(context.guild.id)
        if guild_settings is not None and "default_channel" in guild_settings:
            default_channel = context.bot.get_channel(guild_settings["default_channel"])
            await default_channel.send(response, **keyword_arguments)
        else:
            await context.send(response, **keyword_arguments)
    else:
        await context.send(response, **keyword_arguments)

    # Delete the original message, if requested.
    if delete_original:
        time.sleep(1)
        await context.message.delete()


def load_token(token_file):
    """Load an API token from file."""
    with open(token_file, "r") as open_token_file:
        return open_token_file.read().strip()


async def is_administrator(context):
    """Check if the message author is an administrator."""
    return context.author.guild_permissions.administrator
