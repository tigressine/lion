"""
Generates dog pictures utilizing woofbot.io API

Made by joey
"""

import json
import random
import aiohttp
import discord

COMMAND = "dog"

API_URL = "https://api.woofbot.io/v1/"
API_DOG_URL_FORMAT = "https://api.woofbot.io/v1/breeds/{0}/image"

async def fetch_url(url):
    # Initialize response to be empty
    response = ''
    try:
        session = aiohttp.ClientSession()
        async with session.get(url) as url_response:
            if url_response.status == 200:
                response = await url_response.json()
    finally:
        session.close()

    return response

async def command_dog(client, message):
    breed = message.content.replace("!dog ", "").lower()
    response = ""

    if breed == "!dog":
        # The user didn't request a breed.
        return

    if breed == "breeds":
        # The user requested for list of breeds, let's give that.
        breeds = await get_breeds()
        return await client.send_message(message.channel, breeds) 

    request_url = API_DOG_URL_FORMAT.format(breed)
    

    try:
        web_response = await fetch_url(request_url)

        # Do we have data within web_response?
        if web_response != '':
            response = web_response["response"]["url"]
        else:
            response = "%s are currently not supported 😓... Type `!dog breeds` for a list of breeds the bot currently supports!" % (breed)

    finally:
        await client.send_message(message.channel, response)


async def get_breeds():
    """ Grabs list of breeds that woofbot.io currently supports and formats into a friendly message """
    try:
        url = API_URL.__add__("breeds")
        web_response = await fetch_url(url)

        # Do we have data within web_response?
        if web_response != '':
            breeds = web_response["response"]["breeds"]
            breeds_list = '\n '.join(breeds)

    finally:
        return "Current breeds are: ``` %s ```" % (breeds_list)