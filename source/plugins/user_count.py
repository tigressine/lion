"""Still garbage, will revisit."""
COMMAND = "users"

async def command_user_count(client, message):
    server = next(iter(client.servers))
    await client.send_message(message.channel, str(server.member_count))
