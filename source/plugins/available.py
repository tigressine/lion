async def command_available(client, message):
    response = "```"
    response += "Available commands for LionBot\n"
    response += "!usercount\n"
    response += "   show how many users are on this server"
    response += "```"

    await client.send_message(message.channel, response)
