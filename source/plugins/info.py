"""Display some information about this bot to the screen.

Written by Tiger Sachse.
"""
import discord

COMMAND = "info"

async def command_info(client, message):
    """Display information about the server."""
    response = "Hey there, I'm Lion! Here's a little bit more about me."

    embedded_message = discord.Embed(color=0xffee05)
    embedded_message.add_field(
        name="Creator",
        value="Tiger Sachse",
        inline=False
    )

    embedded_message.add_field(
        name="Contributors",        
        value="Evan Rupert, Hayden Inghem, Caleb Shepard",
        inline=False
    )
    
    embedded_message.add_field(
        name="Version",
        value="1.1.1",
        inline=False
    )

    embedded_message.add_field(
        name="Technologies",
        value=(
            "Written in Python. Relies heavily on the *discord* package "
            + "written by Rapptz. Source code and documentation for this "
            + "package can be found at https://github.com/Rapptz/discord.py."
        ),
        inline=False
    )

    embedded_message.add_field(
        name="Source",
        value="This project is hosted at https://github.com/tgsachse/lion.",
        inline=False
    )
    
    await client.send_message(message.channel, response, embed=embedded_message)
