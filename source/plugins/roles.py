"""Command to show the available roles of a user"""

from discord.utils import get

COMMAND = "roles"
EXCLUDED_ROLES = ['Admin', 'Moderator',
                  'Teaching Assistant', 'TA', '@everyone', 'Suspended', 'suspended']


async def command_roles(client, message):
    try:
        cmd = parse_command(message.content)
        await handle_command(client, message, cmd)
    except Exception as error:
        await client.send_message(message.channel, str(error))


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
        raise Exception(
            'Invalid sub-command given. Run `!roles help` for usage details')


async def show_all_server_roles(client, message):
    role_names = get_all_server_role_names(client)
    resp = '\n'.join(role_names)
    await client.send_message(message.channel, resp)


async def add_roles_to_user(client, message, role_names):
    check_if_role_names_are_available(client, role_names)

    roles = get_roles_from_role_names(client, role_names)

    await client.add_roles(message.author, *roles)

    resp = 'Added roles `{}` to user {}'.format(
        ' '.join(role_names), create_user_mention(message.author))
    await client.send_message(message.channel, resp)


async def remove_roles_from_user(client, message, role_names):
    check_if_role_names_are_available(client, role_names)

    roles = get_roles_from_role_names(client, role_names)

    await client.remove_roles(message.author, *roles)

    resp = 'Removed roles `{}` from user {}'.format(
        ' '.join(role_names), create_user_mention(message.author))
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


def check_if_role_names_are_available(client, role_names):
    available_roles = get_all_server_role_names(client)

    for rn in role_names:
        if rn not in available_roles:
            raise Exception(
                '{} is not an available role. Run `!roles show` to view available roles'.format(rn))


def create_user_mention(user):
    return '<@{}>'.format(user.id)


def get_roles_from_role_names(client, role_names):
    return [get_server_role_by_name(client, rn) for rn in role_names]


def parse_command(message):
    parts = message.split(' ')
    if len(parts) <= 1:
        raise Exception(
            'Roles sub-command not given. Run `!roles help` for usage details')

    return {
        'subcommand': parts[1],
        'roles': parts[2:]
    }


def get_server_role_by_name(client, role_name):
    server = get_server(client)
    return get(server.roles, name=role_name)


def get_all_server_role_names(client):
    server = get_server(client)

    return [r.name for r in server.roles if r.name not in EXCLUDED_ROLES]


def get_server(client):
    return next(iter(client.servers))
