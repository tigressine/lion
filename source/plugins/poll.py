"""Poll plugin for Lion.

Give Lion the functionality to take a poll over a specified amount of time.

Written by Tiger Sachse.
"""
import re
import time
import asyncio
import discord

COMMAND = "poll"
DELIMITER = ", "
MAX_MINUTES = 60
CHOICE_FORMAT = "{0}) {1}"
POLL_HEADER = "**New poll:**"
PROMPT_PATTERN = r"(?P<prompt>.+)"
WINNER_FORMAT = "{0}) {1} [winner]"
RESULTS_HEADER = "**Poll results:**"
CHOICES_PATTERN = r"\((?P<choices>.+)\)"
WAIT_PATTERN = r"(?P<amount>[1-9][0-9]*)"
INTEGER_EMOJIS = ("0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣")
COMMAND_PATTERN = r"^!{0} {1} {2} {3}$".format(
    COMMAND,
    WAIT_PATTERN,
    PROMPT_PATTERN,
    CHOICES_PATTERN
)

async def command_poll(client, message):
    """Create a poll based on specified inputs, then examine the results."""
    command_match = re.match(COMMAND_PATTERN, message.content)

    # Throw an error message if the command syntax is wrong.
    if command_match is None:
        response = "You've got the poll syntax wrong. Try `!help`."
        await message.channel.send(response)

        return

    # Throw an error message if the time requested is too long.
    if int(command_match.group("amount")) > MAX_MINUTES:
        response = (
            "You are asking for too much time. "
            + "I can't remember things for that long!"
        )
        await message.channel.send(response)

        return

    # Split choices by the delimiter and show the help message if
    # too many choices are provided.
    choices = command_match.group("choices").split(DELIMITER)
    if len(choices) > 9:
        response = "You've got too many choices. Keep it below 10."
        await message.channel.send(response)

        return

    prompt = command_match.group("prompt")
    response = get_response(prompt, choices)
    poll_message = await message.channel.send(response)

    # Add reaction integers so members can vote in the poll.
    for integer in range(1, len(choices) + 1):
        await poll_message.add_reaction(INTEGER_EMOJIS[integer])

    # Wait for the poll to complete.
    await asyncio.sleep(int(command_match.group("amount")) * 60)

    # Attempt to find the poll. If it has been popped from the message deque
    # then just return. This is not ideal... see the find_poll_message docstring.
    poll_message = await find_poll_message(message.channel, poll_message)
    if poll_message == None:
        return

    results = get_results(poll_message, prompt, choices)
    await message.channel.send(results)


def get_response(prompt, choices, winners=[]):
    """Get a formatted poll string, with all choices enumerated."""
    if len(winners) == 0:
        response = POLL_HEADER + "\n"
    else:
        response = ""
    response += prompt + "\n```"
    
    for number, choice in enumerate(choices, 1):
        if number in winners:
            response += WINNER_FORMAT.format(number, choice)
        else:
            response += CHOICE_FORMAT.format(number, choice)
        response += "\n"
    response += "```"

    return response


def get_results(message, prompt, choices):
    """Parse the results based on the reaction counts on the original post."""
    highest = 0
    winners = []
    for reaction in message.reactions:
        if reaction.emoji in INTEGER_EMOJIS:
            integer = INTEGER_EMOJIS.index(reaction.emoji)
            if reaction.count > highest:
                winners = [integer]
                highest = reaction.count
            elif reaction.count == highest:
                winners.append(integer)

    return RESULTS_HEADER + "\n" + get_response(prompt, choices, winners)


async def find_poll_message(channel, poll_message):
    """Find the poll message again."""
    return await channel.history(around=poll_message).get(id=poll_message.id)
