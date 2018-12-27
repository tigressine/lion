"""Main driver script for Lion.

This script creates the Discord client interface and provides a hook into
Lion's plugins.

Written by Tiger Sachse.
"""
import re
import sys
import json
import signal
import discord
from plugins import COMMANDS, INLINES, FILTERED_CHANNELS

TOKEN_FILE = "data/token.json"
COMMAND_PATTERN = r"^!(?P<command>[a-zA-Z]+)"

# Create a Discord client to interface with Discord servers.
client = discord.Client()

@client.event
async def on_message(message):
    """Check for commands after each new message."""

    # Skip messages emitted by Lion.
    if message.author == client.user:
        return

    # Check if message is in a filtered channel.
    for filtered_channels in FILTERED_CHANNELS.keys():
        if message.channel.name in filtered_channels:
            await FILTERED_CHANNELS[filtered_channels](client, message)

            return

    # Check message for inline commands.
    for inline in INLINES.keys():
        if re.match(inline, message.content):
            await INLINES[inline](client, message)

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


def load_token():
    """Load Lion's token from a json file."""
    # with open(TOKEN_FILE, "r") as token_file:
    #     token = json.load(token_file)

    #return token
    return 'NTI3ODYxMDQwNjI5ODA5MTUz.DwaVFw.0nTG9hB94T1d_tIVYZrmkWHRYC0'


def handle_signals(signal_number, stack_frame):
    """Gracefully shut down the client."""
    client.close()
    sys.exit(0)


# Fire up the bot.
signal.signal(signal.SIGINT, handle_signals)
signal.signal(signal.SIGTERM, handle_signals)
client.run(load_token())
