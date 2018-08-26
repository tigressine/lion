"""Main driver script for Lion.

This script creates the Discord client interface and provides a hook into
Lion's plugins.

Written by Tiger Sachse.
"""
import re
import json
import discord
from plugins import COMMANDS

COMMAND_PATTERN = r"^!(?P<command>[a-zA-Z]+)"
TOKEN_FILE = "token.json"

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

        # If the command is supported, execute its function. Else call
        # the "help" function.
        if command in COMMANDS.keys():
            await COMMANDS[command](client, message)
        else:
            await COMMANDS["help"](client, message)


@client.event
async def on_ready():
    """Print a message when Lion is ready to go."""
    message = "Lion: Logging in to server \"{0}\" as {1}..."
    server = next(iter(client.servers)).name
    print(message.format(server, client.user.name))


def load_token():
    """"""
    with open(TOKEN_FILE, "r") as token_file:
        token = json.load(token_file)

    return token


# Fire up the bot.
client.run(load_token())
