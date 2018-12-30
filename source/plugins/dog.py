"""
Generates dog pictures utilizing woofbot.io API

Made by joey
"""
import json
import aiohttp
import discord

COMMAND = "dog"

API_URL = "https://api.woofbot.io/v1/"
API_DOG_URL_FORMAT = "https://api.woofbot.io/v1/breeds/{0}/image"
IMAGE_FILE = "/tmp/dog.jpg"

async def fetch_image(url):
    """ Fetches image from a URL. If successful, returns image data, else returns empty string """
    # Initialize response to be empty
    response = ''
    try:
        session = aiohttp.ClientSession()
        async with session.get(url) as url_response:
            if url_response.status == 200:
                response = await url_response.read()
    finally:
        session.close()
        
    return response

async def fetch_json(url):
    """ Fetches json from a URL. If successful, returns json object, else returns empty string """
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
        web_response = await fetch_json(request_url)

        # Do we have data within web_response?
        if web_response != '':
            image_url = web_response["response"]["url"]
            image_contents = await fetch_image(image_url)

            # We need to make sure image_contents actually contains an image.
            if image_contents != "":
                with open(IMAGE_FILE, "wb") as writable_file:
                    writable_file.write(image_contents)
                    await client.send_file(message.channel, IMAGE_FILE)
                
        else:
            response = "%s are currently not supported 😓... Type `!dog breeds` for a list of breeds the bot currently supports!" % (breed)
    
    except Exception:
        response = "Something went wrong 😭"

    finally:
        # Check if we have a response. We won't have a response in the event that
        # everything successfully runs.
        if response != "":
            await client.send_message(message.channel, response)

async def get_breeds():
    """ Grabs list of breeds that woofbot.io currently supports and formats into a friendly message """
    try:
        url = API_URL.__add__("breeds")
        web_response = await fetch_json(url)

        # Do we have data within web_response?
        if web_response != '':
            breeds = web_response["response"]["breeds"]
            breeds_list = '\n '.join(breeds)

    finally:
        return "Current breeds are: ``` %s ```" % (breeds_list)