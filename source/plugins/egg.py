"""Displays the original users message with regional letter indicators.

Inspired by an incident between *NIX and eggplantpatrol.
Written by Caleb-Shepard, kobeeraveendran, Khalil Wehmeyer, and Tiger Sachse.
"""
import re

COMMAND = "egg"
CHARACTER_LIMIT = 2000
RESPONSE_FORMAT = "{0}:\n{1}"
COMMAND_FORMAT = r"^!{0} (?P<rest>.*)$".format(COMMAND)
EGG_DICT = {
    "1": ":one: ", 
    "2": ":two: ",
    "3": ":three: ",
    "4": ":four: ",
    "5": ":five: ",
    "6": ":six: ",
    "7": ":seven: ",
    "8": ":eight: ",
    "9": ":nine: ",
    "0": ":zero: ",
    "!": ":exclamation: "
}

async def command_egg(client, message):
    """Egg a message."""

    # If the message doesn't fit the command syntax or the message is not
    # all ASCII characters, then show the help message.
    command_match = re.match(COMMAND_FORMAT, message.content, re.DOTALL)
    if command_match is None or not is_ascii(command_match.group("rest")):
        syntax_error_response = "Incorrect egg syntax. Try `!help`."
        await client.send_message(message.channel, syntax_error_response)

        return

    # Save all characters and digits in a components list as regional indicators.
    response_components = []
    for char in command_match.group("rest"):
        if char.isspace():
            response_components.append("  ")
        elif char.isalpha():
            response_components.append(
                ":regional_indicator_{0}:".format(char.lower())
            )
        elif char in EGG_DICT:
            response_components.append(EGG_DICT[char])

    # Compress the response components into a string, and add a mention.
    mention = message.author.mention
    response_component_string = "".join(response_components)
    response = RESPONSE_FORMAT.format(mention, response_component_string)

    # Send the mention and response to the client.
    if len(response) < CHARACTER_LIMIT:
        await client.send_message(message.channel, response)

        # Delete the original request.
        await client.delete_message(message)
    else:
        sassy_response = "I can't handle that many characters. You gotta chill fam."
        await client.send_message(message.channel, sassy_response)


def is_ascii(text):
    """Confirm that the given text is all ASCII characters."""
    return len(text) == len(text.encode())
