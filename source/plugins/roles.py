"""Command to show the available roles of a user"""

from discord.utils import get

COMMAND = "roles"


async def command_roles(client, message):
    try:
        cmd = parse_command(message.content)
        await handle_command(client, message, cmd)
    except Exception as error:
        await client.send_message(message.channel, str(error))
        await command_roles_help(client, message)
        raise error


async def handle_command(client, message, command):
    sub_command = command['subcommand']
    if sub_command == 'help':
        await command_roles_help(client, message)
    elif sub_command == 'show':
        await show_all_server_roles(client, message)
    elif sub_command == 'add':
        await add_roles_to_user(client, message, command['roles'])
    elif sub_command == 'remove':
        await remove_roles_from_user(client, message, command['roles'])
    else: 
        raise Exception('Invalid sub-command given')


async def show_all_server_roles(client, message):
    role_names = get_all_server_role_names(client)
    resp = '\n'.join(role_names)
    await client.send_message(message.channel, resp)


async def add_roles_to_user(client, message, role_names):
    roles = get_roles_from_role_names(client, role_names)

    await client.add_roles(message.author, *roles)

    resp = 'Added roles `{}` to user {}'.format(' '.join(role_names), create_user_mention(message.author))
    await client.send_message(message.channel, resp)



async def remove_roles_from_user(client, message, role_names):
    roles = get_roles_from_role_names(client, role_names)

    await client.remove_roles(message.author, *roles)

    resp = 'Removed roles `{}` from user {}'.format(' '.join(role_names), create_user_mention(message.author))
    await client.send_message(message.channel, resp)


async def command_roles_help(client, message):
    help_message = """
    Available sub-commands for roles:
    **show**:
        displays the available roles in the server
    **add [roles]**:
        gives the user the roles specified
    **remove [roles]**:
        removes the user from the roles specified
    **help**:
        displays this message
    """
    await client.send_message(message.channel, help_message)


def create_user_mention(user):
    return '<@{}>'.format(user.id)


def get_roles_from_role_names(client, role_names):
    return list(map(lambda role_name : get_server_role_by_name(client, role_name), role_names))


def parse_command(message):
    parts = message.split(' ')
    if len(parts) <= 1:
        raise Exception('Roles sub-command not given')

    return {
        'subcommand': parts[1],
        'roles': parts[2:]
    }


def get_server_role_by_name(client, role_name):
    server = get_server(client)
    return get(server.roles, name=role_name)



def get_all_server_role_names(client):
    server = get_server(client)
    names = list(map(lambda r: r.name, server.roles))
    names.remove('@everyone')
    return names

def get_server(client):
    return next(iter(client.servers))
