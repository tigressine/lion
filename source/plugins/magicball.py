import json
import random
import discord
import re
COMMAND = "8ball"

COMMAND_PATTERN = r"^\!{0}( (?P<question>[a-zA-Z ]([^\"]+)+))?$".format(COMMAND)
"""This prints out the messages to see if the json is loaded"""
debug = False


async def command_magicball(client,message):
    """See if !magic (message) matches the regex pattern above.
    This also allows for easy string extraction from message"""
    command_match = re.match(COMMAND_PATTERN, message.content)

    response = command_match.group("question")

    if response is None:
        response = "Magic 8 ball says:"
    """JSON to a 2d array"""
    with open("data/8ball_responses.json") as f:
        data = json.load(f)

    if debug:
        print(data["magicball"][random.randint(0, len(data["magicball"]))])

    """Embedded Discord message creation"""
    embed = discord.Embed(color=0x6105ff)

    embed.set_author(
        name="Magic Ball of Fortune", icon_url = "https://cdn.discordapp.com/attachments/353269187633741824/532808475781234688/61F8HIGkUiL.png")

    embed.add_field(name=response, value=data["magicball"][random.randint(0, len(data["magicball"]))], inline=False)

    await message.channel.send(embed=embed)

