"""Displays the original users message in regional letter indicators.
Inspired by an incident between *NIX and eggplantpatrol.

Written by Caleb-Shepard and kobeeraveendran.
Some data structure revision by Khalil Wehmeyer.
Small updates by Tiger Sachse.
"""
import re
import nltk

COMMAND = "egg"
COMMAND_FORMAT = r"^!{0} (?P<rest>.*)$".format(COMMAND)
MAX_MESSAGE_LENGTH = 1000
EGG_DICT = {
    '1': ':one:', 
    '2': ':two:',
    '3': ':three:',
    '4': ':four:',
    '5': ':five:',
    '6': ':six:',
    '7': ':seven:',
    '8': ':eight:',
    '9': ':nine:',
    '0': ':zero:',
    '!': ':exclamation:'
}

def is_ascii(text):
    """Confirm that the given text is all ASCII characters."""
    return len(text) == len(text.encode())


async def command_egg(client, message):
    """Egg a message."""

    # If the message doesn't fit the command syntax or the message is not
    # all ASCII characters, then show the help message.
    command_match = re.match(COMMAND_FORMAT, message.content, re.DOTALL)
    if command_match is None or not is_ascii(command_match.group("rest")):
        syntax_error_response = "Incorrect egg syntax. Try `!help`."
        await client.send_message(message.channel, syntax_error_response)

        return

    # Figure out who sent the command.
    message_author_display_name = message.author.display_name
    message_body = command_match.group("rest")

    # Begin generating our response to the sender; this will be a list of words
    # rather than a string to simplify, beautify, and optimize message splits
    # when the character limit is surpassed. Messages will be split by word
    # and never mid-word unless if absolutely neccessary.
    full_response = []
    response = ""
    tokenized_message = nltk.word_tokenize(message_body)

    # Dictionary remapping of individual chatacters to their egg representation.
    for word in tokenized_message:

        # Convert a word into its egg representation.
        egg_word = ""
        for char in word:
            if not is_ascii(char):
                pass
            elif char.isalpha():
                egg_word += ":regional_indicator_" + char.lower() + ": "
            elif char in EGG_DICT:
                egg_word += EGG_DICT[char] + ' '

        if len(egg_word) + len(response) < MAX_MESSAGE_LENGTH:
            response += egg_word
        else:

            # Save one (1000 character or less) section of the message
            # so that the message may be split into different parts.
            full_response.append(response)

            # Reset the value of "response" and continue.
            response = ""

        response += "   "

    # If the sender signature fits in the resulting message without overflowing
    # to a new message, then add it to the end. Otherwise just send it separately.
    if len(response + " - " + message_author_display_name) < MAX_MESSAGE_LENGTH:
        response += " - " + message_author_display_name
        full_response.append(response)
    else:
        full_response.append(" - " + message_author_display_name)


    # There may be more than one message to send, so loop through the full response
    # and send each message sequentially.
    for response in full_response:
        await client.send_message(message.channel, response)
