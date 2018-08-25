#import sqlite
import re
import discord
import random
from constants import TOKEN, FULL_PATTERN, FLAG, COMMAND

# GOALS
# count messages (and subtract from count as they are deleted)
# allow autoroles with commands
# create queue of requests that can be parsed by the mods

print(FULL_PATTERN)
PATTERN = re.compile(FULL_PATTERN)

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    result = PATTERN.match(message.content)
    print(result)
    if result is not None:
        print(True)
        command = result.group(COMMAND)
        if command == "roll":
            result2 = re.match("^[0-9]+$", result.group(FLAG))
            if result2:
                max_roll = int(result.group(FLAG))
                roll = random.choice(range(max_roll))
                response = "You rolled a {0}".format(roll)
                await client.send_message(message.channel, response)
            else:
                await client.send_message(message.channel, "cant bub")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
