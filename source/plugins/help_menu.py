"""Produce a modest help menu that lists high level commands.

Written by Tiger Sachse.
"""
import discord

COMMAND = "help"

async def command_help_menu(client, message):
    """Display an embedded help menu."""
    response = "Hey there! Here's a list of commands that I understand:"

    embedded_message = discord.Embed(color=0x81f97c)
    embedded_message.add_field(
        name="!users",
        value="Display the latest server membership count.",
        inline=False
    )

    embedded_message.add_field(
        name="!poll time \"prompt\" \"choice1|choice2|choice3|etc\"",        
        value="Create a new poll. Time is in minutes.",
        inline=False
    )

    embedded_message.add_field(
        name="!garage [garage]",
        value="See the status of the UCF parking garages.",
        inline=False
    )

    embedded_message.add_field(
        name="!listroles",
        value="List all server roles.",
        inline=False
    )

    embedded_message.add_field(
        name="!addrole [roles...]",
        value="Give yourself a language role.",
        inline=False
    )

    embedded_message.add_field(
        name="!removerole [roles...]",
        value="Remove your language roles.",
        inline=False
    )

    embedded_message.add_field(
      name="!corgi",
      value="Call a good boy over for pets.",
      inline=False
    )
    
    embedded_message.add_field(
        name="!sponge message",
        value="Create a spicy, sarcastic meme.",
        inline=False
    )

    await client.send_message(message.channel, response, embed=embedded_message)
