"""Displays the server's user count.

Written by Tiger Sachse.
"""
COMMAND = "users"

async def command_user_count(client, message):
    """Display the server's user count."""
    server = next(iter(client.servers))
    response = "This server has {0} members.".format(server.member_count)
    await client.send_message(message.channel, response)
