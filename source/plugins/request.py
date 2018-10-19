"""Command to queue server requests and send them to the admins"""

import json
import re

# TODO: Create function for interacting with the request_data file by taking a lambda to perform on the data
# TODO: Look for other ways to refactor this code to be more understandable

REQUEST_COMMAND = "request"
SHOW_COMMAND = "showrequests"
RESPOND_COMMAND = "respond"

REQUEST_DATA_FILE_PATH = "data/request_data.json"
DEFAULT_RESPONSE = "Thank you for submitting your request, the admins will review it shortly"


async def command_request(client, message):
    try:
        request = create_request_item(message)
        add_request(request)
        await client.send_message(message.channel, DEFAULT_RESPONSE)
    except Exception as error:
        await client.send_message(message.channel, str(error))
        raise error


async def command_show_requests(client, message):
    try:
        resp = get_requests_list_message()
        await client.send_message(message.channel, resp)
    except Exception as error:
        await client.send_message(message.channel, str(error))
        raise error


async def command_respond(client, message):
    try:
        cmd = parse_respond_command(message.content)
        remove_request(cmd['request_index'])
        await send_respond_response(client, cmd)
    except Exception as error:
        await client.send_message(message.channel, str(error))
        raise error


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


def add_request(request):
    with open(REQUEST_DATA_FILE_PATH, 'r+') as file:
        requests = json.load(file)
        file.seek(0)
        file.write(json.dumps(requests + [request]))
        file.truncate()


def remove_request(index):
    with open(REQUEST_DATA_FILE_PATH, 'r+') as file:
        requests = json.load(file)
        del requests[index]
        file.seek(0)
        file.write(json.dumps(requests))
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
    with open(REQUEST_DATA_FILE_PATH, 'r') as requests_data_file:
        return json.load(requests_data_file)
