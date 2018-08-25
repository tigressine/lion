"""Main script for Lion.

This script creates the Discord client interface and provides a hook into the
plugins installed alongside Lion.
Written by Tiger Sachse.
"""
import re
import discord
from plugins import commands
from constants import TOKEN, COMMAND_PATTERN

# Create a Discord client to interface with Discord servers.
client = discord.Client()

@client.event
async def on_message(message):
    """Check for commands after each new message."""

    # Skip messages emitted by Lion.
    if message.author == client.user:
        return

    command_match = re.match(COMMAND_PATTERN, message.content)
    if command_match is not None:
        command = command_match.group("command")

        # if the command is supported, execute its function. Else call
        # the "available" commands function.
        if command in commands.keys():
            await commands[command](client, message)
        else:
            await commands["available"](client, message)


@client.event
async def on_ready():
    """Print a message when Lion is ready to go."""
    message = "Lion: Logging in to server \"{0}\" as {1}..."
    server = next(iter(client.servers)).name
    print(message.format(server, client.user.name))


# Fire up the bot.
client.run(TOKEN)
