"""Plugin to manage one's own non-critical roles.

Written by Evan Rupert and Tiger Sachse.
"""
import re
import discord

ADD_COMMAND = "addroles"
LIST_COMMAND = "listroles"
REMOVE_COMMAND = "removeroles"
HAS_ROLE_FORMAT = "--> {0}"
LACKS_ROLE_FORMAT = "    {0}"
LIST_HEADER = "**All server roles:**"
LIST_COMMAND_PATTERN = r"^!{0}$".format(LIST_COMMAND)
ADD_COMMAND_PATTERN = r"^!{0}( \S+)+$".format(ADD_COMMAND)
REMOVE_COMMAND_PATTERN = r"^!{0}( \S+)+$".format(REMOVE_COMMAND)
PERMISSIONS_ERROR = "Insufficent permissions to handle one of your specified roles."

async def command_addroles(client, message):
    """Give the member new roles."""
    roles = await get_roles(client, message, ADD_COMMAND, ADD_COMMAND_PATTERN)
    if roles is None:
        return

    try:
        await client.add_roles(message.author, *roles)
        response = "Added roles! Check them out with `!{0}`".format(LIST_COMMAND)
        await client.send_message(message.channel, response)
    except discord.errors.Forbidden:
        await client.send_message(message.channel, PERMISSIONS_ERROR)


async def command_removeroles(client, message):
    """Remove roles from the member."""
    roles = await get_roles(client, message, REMOVE_COMMAND, REMOVE_COMMAND_PATTERN)
    if roles is None:
        return

    try:
        await client.remove_roles(message.author, *roles)
        response = "Removed roles. Confirm with `!{0}`".format(LIST_COMMAND)
        await client.send_message(message.channel, response)
    except discord.errors.Forbidden:
        await client.send_message(message.channel, PERMISSIONS_ERROR)


async def command_listroles(client, message):
    """List all roles available on the server."""
    response = get_response(get_server(client), message.author)

    await client.send_message(message.channel, response)


async def get_roles(client, message, command, command_pattern):
    """Get all available roles on the server."""

    # First, confirm that the message matches the syntax.
    command_match = re.match(command_pattern, message.content)
    if command_match is None:
        response = "You've got the {0} syntax wrong. Try `!help`.".format(command)
        await client.send_message(message.channel, response)

        return None

    # Get all possible roles, and all desired role names from the message content.
    possible_roles = [role for role in get_server(client).roles]
    role_names = set(message.content.split()[1:])

    # Ensure every desired role name is also a possible role. Also save the
    # roles that correspond to the given role names in a list.
    roles = []
    for name in role_names:
        for possible_role in possible_roles:
            if name.lower() == possible_role.name.lower():
                roles.append(possible_role)
                break
        else:
            response = "`{0}` is not a role. Try `!{1}`.".format(name, LIST_COMMAND)
            await client.send_message(message.channel, response)

            return None

    return roles


def get_server(client):
    """Get the next (and only) server for the client."""
    return next(iter(client.servers))


def get_response(server, author):
    """Get a formatted roles list string, with all current roles marked."""
    response = LIST_HEADER + "\n```"
    
    for role in server.roles:
        if role in author.roles:
            response += HAS_ROLE_FORMAT.format(role.name)
        else:
            response += LACKS_ROLE_FORMAT.format(role.name)
        response += "\n"
    response += "```"
    response += "\nYour roles are highlighted with an arrow!"

    return response
