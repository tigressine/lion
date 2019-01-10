"""Displays the server's user count.

Written by Tiger Sachse.
Inspired by Discord-User-Counter by Eric Woolard.
"""
COMMAND = "users"
RESPONSE_FORMAT = "**This server has {0} members ({1} currently online).**"

async def command_user_count(client, message):
    """Display the server's user count."""
    server = next(iter(client.guilds))

    active_members = 0
    for member in server.members:
        status = str(member.status)
        if status != "offline":
            active_members += 1

    response = RESPONSE_FORMAT.format(server.member_count, active_members)
    await message.channel.send(response)
