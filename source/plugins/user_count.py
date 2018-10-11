"""Still garbage, will revisit."""
COMMAND = "users"

async def command_user_count(client, message):
    server = next(iter(client.servers))
    response = "This server has {0} members.".format(server.member_count)
    await client.send_message(message.channel, response)
