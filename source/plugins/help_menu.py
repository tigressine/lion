"""Produce a modest help menu that lists high level commands.

Written by Tiger Sachse.
"""
import discord

COMMAND = "help"

async def command_help_menu(client, message):
    """Display an embedded help menu."""
    response = "Here's a list of commands that I understand..."

    embedded_message = discord.Embed(color=0xffee05)
    embedded_message.add_field(
        name="!info",
        value="Show some more information about Shell (Lion).",
        inline=False
    )

    embedded_message.add_field(
        name="!users",
        value="Display the latest server membership count.",
        inline=False
    )

    embedded_message.add_field(
        name="!poll time prompt (choice1, choice2, etc)",        
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
        name="!addroles [roles...]",
        value="Give yourself some new language roles.",
        inline=False
    )

    embedded_message.add_field(
        name="!removeroles [roles...]",
        value="Remove language roles.",
        inline=False
    )

    embedded_message.add_field(
      name="!dog [breed]",
      value="Get a picture of a good boy!",
      inline=False
    )

    embedded_message.add_field(
        name="!8ball message",
        value="Your questions will be answered by an object of irrelevance.",
        inline=False
    )

    embedded_message.add_field(
        name="!sponge message",
        value="Create a spicy, sarcastic meme.",
        inline=False
    )

    embedded_message.add_field(
        name="!egg message",
        value="Send your text through the egg machine.",
        inline=False
    )
    
    embedded_message.add_field(
        name="!weather [city|zip]",
        value="Check the current weather forecast.",
        inline=False
    )

    embedded_message.add_field(
        name="!listclasses",
        value="List all class channels",
        inline=False
    )

    embedded_message.add_field(
        name="!register [class_names...]",
        value="Register for classes, allowing access their channels",
        inline=False
    )

    embedded_message.add_field(
        name="!unregister [class_names...]",
        value="Unregister from classes, hiding their channels",
        inline=False
    )

    await message.channel.send(response, embed=embedded_message)
