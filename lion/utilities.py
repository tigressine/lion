"""A collection of utility functions for Lion.

Written by Tiger Sachse.
"""
async def throw_error(context, error, message=None):
    """Send an error to the context's server.
    
    If a message is provided, that message is included in the post, otherwise
    the error's default message is included.
    """
    ERROR_FORMAT = ("Something went wrong!\n```\n"
                    "Command : {0}\n"
                    "Error   : {1}\n"
                    "Message : {2}\n```")

    response = ERROR_FORMAT.format(context.command,
                                   type(error).__name__,
                                   message if message is not None else error)
    await respond(context, response)


async def respond(
    context,
    message,
    ignore_formatting=False,
    delete_original=True,
    **keyword_arguments):
    """Respond to a message in context.
    
    The response is automatically formatted with the original message's author's
    handle, although this can be disabled with the ignore_formatting flag.
    """
    RESPONSE_FORMAT = "{0}:\n{1}"

    # Avoid additionally formatting, if requested.
    if ignore_formatting:
        response = message
    else:
        response = RESPONSE_FORMAT.format(context.author.mention, message)

    await context.send(response, **keyword_arguments)

    # Delete the original message by default.
    if delete_original:
        await context.message.delete()


def load_token(token_name):
    """Load an API token from file."""
    with open(token_name, "r") as token_file:
        return token_file.read().strip()
