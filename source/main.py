#import sqlite
import re
import discord
from constants import TOKEN, COMMAND_PATTERN
# GOALS
# count messages (and subtract from count as they are deleted)
# allow autoroles with commands
# create queue of requests that can be parsed by the mods

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_match = re.match(COMMAND_PATTERN, message.content)
    if message_match:
        print("match")
        flag = message_match.group('flag')
        print(flag)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
