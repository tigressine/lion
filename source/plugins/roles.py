"""Plugin to manage one's own non-critical roles.

Written by Evan Rupert.
Revised by Tiger Sachse.
"""

import re

ADD_COMMAND = "addrole"
REMOVE_COMMAND = "removerole"
LIST_COMMAND = "listroles"
EXCLUDED_ROLES_FILE = "data/excluded_roles.txt"
LIST_COMMAND_PATTERN = r"^!{0}$".format(LIST_COMMAND)
ADD_COMMAND_PATTERN = r"^!{0}( [a-zA-Z]+)+$".format(ADD_COMMAND)
REMOVE_COMMAND_PATTERN = r"^!{0}( [a-zA-Z]+)+$".format(REMOVE_COMMAND)

async def command_addrole(client, message):
    roles = await get_roles(client, message, ADD_COMMAND, ADD_COMMAND_PATTERN)
    if roles is None:
        return

    await client.add_roles(message.author, *roles)

    response = "Added roles! Check them out with !{0}".format(LIST_COMMAND)
    await client.send_message(message.channel, response)


async def command_removerole(client, message):
    roles = await get_roles(client, message, REMOVE_COMMAND, REMOVE_COMMAND_PATTERN)
    if roles is None:
        return

    await client.remove_roles(message.author, *roles)

    response = "Removed roles. Confirm with !{0}".format(LIST_COMMAND)
    await client.send_message(message.channel, response)


async def get_roles(client, message, command, command_pattern):
    command_match = re.match(command_pattern, message.content)
    if command_match is None:
        response = "You've got the {0} syntax wrong. Try `!help`.".format(command)
        await client.send_message(message.channel, response)

        return None

    possible_roles = get_possible_roles(client)
    role_names = set(message.content.split()[1:])

    roles = []
    for name in role_names:
        for possible_role in possible_roles:
            if name == possible_role.name:
                roles.append(possible_role)
                break
        else:
            response = "`{0}` is not a role. Try `!{1}`.".format(name, LIST_COMMAND)
            await client.send_message(message.channel, response)

            return None

    return roles


def get_server(client):
    return next(iter(client.servers))


def get_possible_roles(client):
    with open(EXCLUDED_ROLES_FILE, "r") as role_file:
        excluded_roles = role_file.readlines()

    server = get_server(client)

    return [role for role in server.roles if role.name not in excluded_roles]

"""
async def show_all_server_roles(client, message):
    role_names = get_all_server_role_names(client)
    resp = '\n'.join(role_names)
    await client.send_message(message.channel, resp)

def get_roles_from_role_names(client, role_names):
    return [get_server_role_by_name(client, rn) for rn in role_names]
"""
