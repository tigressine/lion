import json
import random
import discord
import re
import os
from plugins import egg

COMMAND = "8ball"
COMMAND_PATTERN = r"^\!{0}( (?P<question>[a-zA-Z ]([^\"]+)+))?$".format(COMMAND)
"""This prints out the messages to see if the json is loaded"""

COLORS = {
    "positive": 0x008000,
    "neutral": 0xffee05,
    "negative": 0xff0000
}


async def command_magicball(client,message):
    """See if !8ball (message) matches the regex pattern above.
    This also allows for easy string extraction from message"""
    command_match = re.match(COMMAND_PATTERN, message.content)

    if len(message.content) > (1+len(COMMAND)):
        if command_match is None or not egg.is_ascii(command_match.group("question")):
            syntax_error_response = "Incorrect 8 ball syntax. Try `!help`."
            await message.channel.send(syntax_error_response)

            return

    response = command_match.group("question")
    if response is None:
        response = "Magic 8 ball says:"
    
    """JSON to a 2d array"""
    with open("data/8ball_responses.json") as f:
        data = json.load(f)
    fortune = data[random.randrange(len(data))]

    """Embedded Discord message creation"""
    embed = discord.Embed(color=COLORS[fortune[1].lower()])

    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/532378760893169664/540981908218183701/magicball48.png")

    embed.add_field(name=response, value=fortune[0], inline=False)

    await message.channel.send(embed=embed)
