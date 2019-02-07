async def throw_error(context, error, message=None):
    response = ("Something went wrong!\n```\n"
                "Command : {0}\n"
                "Error   : {1}\n"
                "Message : {2}\n"
                "```").format(context.command,
                              type(error).__name__,
                              message if message is not None else error)
    await context.send(response)
