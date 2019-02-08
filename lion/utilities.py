import logging

async def throw_error(context, error, message=None):
    """"""
    ERROR_FORMAT = ("Something went wrong!\n```\n"
                    "Command : {0}\n"
                    "Error   : {1}\n"
                    "Message : {2}\n"
                    "```")

    response = ERROR_FORMAT.format(context.command,
                                   type(error).__name__,
                                   message if message is not None else error)
    await context.send(response)


async def respond(context,
                  message,
                  ignore_formatting=False,
                  delete_original=True,
                  **keyword_arguments):
    """"""
    RESPONSE_FORMAT = "{0}:\n{1}"

    if ignore_formatting:
        response = message
    else:
        response = RESPONSE_FORMAT.format(context.author.mention, message)

    await context.send(response, **keyword_arguments)

    if delete_original:
        await context.message.delete()


def load_token(token_name):
    """Load the Discord API authentication token."""
    with open(token_name, "r") as token_file:
        return token_file.read().strip()
