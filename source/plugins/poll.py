"""Poll plugin for Lion.

Give Lion the functionality to take a poll over a specified amount of time.

Written by Tiger Sachse.
"""
import re
import time
import asyncio
import discord

COMMAND = "poll"
DELIMITER = ";"
MAX_SECONDS = 172800
CHOICE_FORMAT = "{0}) {1}"
WINNER_FORMAT = "**{0}) {1} [winner]**"
PROMPT_PATTERN = r"`(?P<prompt>.+)`"
CHOICES_PATTERN = r"`(?P<choices>.+)`"
WAIT_PATTERN = r"(?P<amount>[1-9][0-9]*)(?P<multiplier>[smhd])"
INTEGER_EMOJIS = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]

COMMAND_PATTERN = r"^!{0} {1} {2} {3}$".format(COMMAND,
                                               WAIT_PATTERN,
                                               PROMPT_PATTERN,
                                               CHOICES_PATTERN)

async def command_poll(client, message):
    """Create a poll based on specified inputs, then examine the results."""
    command_match = re.match(COMMAND_PATTERN, message.content)

    # Call the help command if the given message does not match
    # the command pattern.
    if command_match is None:
        await command_poll_help(client, message)
        return

    # Get the wait time specified in the message.
    wait = get_wait(command_match.group("amount"),
                    command_match.group("multiplier"))

    # Split choices by the delimiter and show the help message if
    # too many choices are provided.
    choices = command_match.group("choices").split(DELIMITER)
    if len(choices) > 9:
        await command_poll_help(client, message)
        return

    prompt = command_match.group("prompt")
    response = get_response(prompt, choices)
    poll_message = await client.send_message(message.channel, response)

    # Add reaction integers so members can vote in the poll.
    for integer in range(1, len(choices) + 1):
        await client.add_reaction(poll_message, INTEGER_EMOJIS[integer])

    # Wait for the poll to complete.
    await asyncio.sleep(wait)

    # Attempt to find the poll. If it has been popped from the message deque
    # then just return. This is not ideal... see the find_poll_message docstring.
    poll_message = find_poll_message(client, response)
    if poll_message == None:
        return

    results = get_results(poll_message, prompt, choices)
    await client.send_message(message.channel, results)


# UNFINISHED
async def command_poll_help(client, message):
    """Show a help menu for the poll command."""
    await client.send_message(message.channel, "bad")
###########


def get_wait(amount, multiplier):
    """Get the wait time for a poll based on the amount and the multiplier."""
    wait = int(amount)

    if multiplier == "s":
        wait *= 1
    elif multiplier == "m":
        wait *= 60
    elif multiplier == "h":
        wait *= 3600
    elif multiplier == "d":
        wait *= 86400

    return wait if wait < MAX_SECONDS else MAX_SECONDS


def get_response(prompt, choices, winners=[]):
    """Get a formatted poll string, with all choices enumerated."""
    response = prompt + "\n\n"
    
    for number, choice in enumerate(choices, 1):
        if number in winners:
            response += WINNER_FORMAT.format(number, choice)
        else:
            response += CHOICE_FORMAT.format(number, choice)

        if number < len(choices):
            response += "\n"

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

    return "__Results:__\n" + get_response(prompt, choices, winners)


def find_poll_message(client, text):
    """Search from the back of the deque forward for the poll.
    
    This is not an ideal solution, but message objects do not appear
    to update with new reactions and waiting for reactions causes problems,
    so it is necessary to hunt down the message again in the deque. Reversing
    the deque returns a reversed iterator which is quite time and memory
    efficient. This could fail if more than MAX_MESSAGES are produced in the
    poll's time frame.
    """
    return discord.utils.get(reversed(client.messages), content=text)
