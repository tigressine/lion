"""Still garbage, will revisit."""
COMMAND = "help"

async def command_help_menu(client, message):
    response = "```"
    response += "Available commands for Lion\n"
    response += "!usercount\n"
    response += "   show how many users are on this server"
    response += "```"

    await client.send_message(message.channel, response)
