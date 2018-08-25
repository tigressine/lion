import re
import discord
from plugins import commands
from constants import TOKEN#, FULL_PATTERN, FLAG, COMMAND

client = discord.Client()

@client.event
async def on_message(message):

    # Skip messages emitted by LionBot.
    if message.author == client.user:
        return

    pattern = r"^!(?P<command>[a-zA-Z]+)"
    match_result = re.match(pattern, message.content)
    if match_result is not None:
        command = match_result.group("command")
        print(command)
        if command in commands.keys():
            await commands[command](client, message)
        else:
            await commands["help"](client, message)

@client.event
async def on_ready():
    message = "LionBot: Logging in to server \"{0}\" as {1}..."
    server = next(iter(client.servers)).name
    
    print(message.format(server, client.user.name))


client.run(TOKEN)

"""
"""

"""
print(FULL_PATTERN)
PATTERN = re.compile(FULL_PATTERN)
"""

"""
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
"""


