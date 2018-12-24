"""Command to queue server requests and send them to the admins.

Written by Evan Rupert.
"""

import json
import re
import os.path
from discord.utils import get


REQUEST_COMMAND = "request"
REQUESTS_COMMAND = "requests"
RESPOND_COMMAND = "respond"

REQUEST_DATA_FILE_PATH = "data/request_data.json"
DEFAULT_RESPONSE = "Thank you for submitting your request, the admins will review it shortly"
NO_PERMISSIONS_RESPONSE = "You do not have the proper permissions to perform this action"
ADMIN_CHANNEL_NAME = "admins"
ELEVATED_PERMISSIONS_ROLES = ['Admin', 'Moderator']


async def command_request(client, message):
    try:
        await handle_request_command(client, message)
    except Exception as error:
        await client.send_message(message.channel, str(error))
        raise error


async def command_requests_management(client, message):
    try:
        await check_user_has_elevated_permissions(client, message,
                                                  lambda: handle_requests_management_command(client, message))
    except Exception as error:
        await client.send_message(message.channel, str(error))
        raise error


async def command_respond(client, message):
    try:
        await check_user_has_elevated_permissions(client, message,
                                                  lambda: handle_respond_command(client, message))
    except Exception as error:
        await client.send_message(message.channel, str(error))
        raise error


async def check_user_has_elevated_permissions(client, message, action):
    if user_has_elevated_permissions(message.author):
        await action()
    else:
        await client.send_message(message.channel, NO_PERMISSIONS_RESPONSE)


async def handle_request_command(client, message):
    request = create_request_item(message)
    add_request(request)
    await alert_admins(client, message, request)
    await client.send_message(message.channel, DEFAULT_RESPONSE)


async def handle_requests_management_command(client, message):
    command = parse_sub_command(message.content)

    if command['subcommand'] == 'show':
        await client.send_message(message.channel, get_requests_list_message())
    elif command['subcommand'] == 'clear':
        clear_requests()
        await client.send_message(message.channel, 'The requests queue has been cleared')


async def handle_respond_command(client, message):
    cmd = parse_respond_command(message.content)
    remove_request(cmd['request_index'])
    await send_respond_response(client, cmd)
    await client.send_message(message.channel, 'The response has been sent')


async def alert_admins(client, message, request):
    admin_channel = get(message.server.channels, name=ADMIN_CHANNEL_NAME)
    resp = 'New request "{}" by **{}**'.format(
        request['message'], request['author_name'])
    await client.send_message(admin_channel, resp)


async def send_respond_response(client, cmd):
    request = cmd['request']
    resp = '<@{}> Your request "{}" has been considered and the response is: "{}"'.format(
        request['author_id'], request['message'], cmd['message'])

    channel = client.get_channel(request['channel_id'])
    await client.send_message(channel, resp)


def parse_respond_command(content):
    parts = content.split(' ')

    if parts[0] == '!respond':
        num = 0
    else:
        num = re.search(r'\[(.+?)\]', parts[0]).group(1)

    return {
        'message': ' '.join(parts[1:]),
        'request_index': int(num),
        'request': get_requests()[int(num)]
    }


def parse_sub_command(content):
    parts = content.split(' ')
    if len(parts) <= 1:
        raise Exception(
            'Requests sub-command not given. Run `!requests help` for usage details')

    return {
        'subcommand': parts[1],
    }


def user_has_elevated_permissions(user):
    user_elevated_permissions = [
        role.name for role in user.roles if role.name in ELEVATED_PERMISSIONS_ROLES]

    return user_elevated_permissions != []


def add_request(request):
    map_over_requests(lambda reqs: [request] + reqs)


def remove_request(index):
    map_over_requests(lambda reqs: remove_element(reqs, index))


def clear_requests():
    map_over_requests(lambda _: [])


def remove_element(l, idx):
    return l[:idx] + l[idx+1:]


def map_over_requests(f):
    if not requests_file_exists():
        with open(REQUEST_DATA_FILE_PATH, 'w') as file:
            requests = f([])
            file.write(json.dumps(requests))

        return

    with open(REQUEST_DATA_FILE_PATH, 'r+') as file:
        requests = json.load(file)
        file.seek(0)
        updated_requests = f(requests)
        file.write(json.dumps(updated_requests))
        file.truncate()


def create_request_item(message):
    return {
        'message': get_request_message(message.content),
        'author_id': message.author.id,
        'author_name': message.author.name,
        'channel_id': message.channel.id,
    }


def get_request_message(content):
    parts = content.split(' ')
    return ' '.join(parts[1:])


def get_requests_list_message():
    request_messages = [request_display_string(
        i, req) for i, req in enumerate(get_requests())]
    if request_messages:
        return '\n'.join(request_messages)
    else:
        return 'There are no current requests in the queue.  You are all good'


def request_display_string(index, request):
    return '[{}] "{}" by **{}**'.format(index, request['message'], request['author_name'])


def get_requests():
    if not requests_file_exists():
        return []

    with open(REQUEST_DATA_FILE_PATH, 'r') as requests_data_file:
        return json.load(requests_data_file)


def requests_file_exists():
    return os.path.isfile(REQUEST_DATA_FILE_PATH)
