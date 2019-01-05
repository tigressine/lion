"""Generate dog pictures utilizing woofbot.io API.

Made by joey.
Edited by Tiger Sachse.
"""
import re
import json
import aiohttp
import discord

COMMAND = "dog"
IMAGE_FILE = "/tmp/dog.jpg"
API_URL = "https://api.woofbot.io/v1/"
API_DOG_URL_FORMAT = "https://api.woofbot.io/v1/breeds/{0}/image"
COMMAND_PATTERN = r"^!{0}( (?P<breed>[a-zA-Z ]+))?$".format(COMMAND)

async def command_dog(client, message):
    """Fetch a dog picture from the Internet!"""
    command_match = re.match(COMMAND_PATTERN, message.content)

    # If the given command doesn't match the necessary pattern, we've got a problem.
    if command_match is None:
        response = "You've got the dog syntax wrong. Try `!help`."
        await client.send_message(message.channel, response)

        return
    
    # Get a list of available breeds.
    breeds = await get_breeds()
    requested_breed = command_match.group("breed")
  
    # If no breed was requested, return a list of breeds.
    if requested_breed is None:
        await client.send_message(message.channel, make_breeds_list(breeds)) 

        return
    
    # Ensure that the requested breed is available in the API. If not, cry about it.
    requested_breed = requested_breed.lower()
    for breed in breeds:
        if requested_breed == breed.lower():
            break
    else:
        response = "That breed isn't currently available!\n" + make_breeds_list(breeds)
        await client.send_message(message.channel, response)

        return

    request_url = API_DOG_URL_FORMAT.format(requested_breed)
    request_json = await fetch_json(request_url)

    if request_json is not None:
        image = await fetch_image(request_json["response"]["url"])

        if image is not None:
            with open(IMAGE_FILE, "wb") as writable_file:
                writable_file.write(image)
            
            await client.send_file(message.channel, IMAGE_FILE)
        else:
            await client.send_message(message.channel, "Could not download image!")
    else:
        await client.send_message(message.channel, "Could not reach Woofbot API.")


async def fetch_image(url):
    """Fetch an image from a URL.
    
    If successful, return image data, else return an empty string
    """
    session = aiohttp.ClientSession()
    async with session.get(url) as url_response:
        if url_response.status == 200:
            response = await url_response.read()
    session.close()
        
    return response


async def fetch_json(url):
    """Get a JSON object from a URL."""
    session = aiohttp.ClientSession()
    async with session.get(url) as url_response:
        if url_response.status == 200:
            response = await url_response.json()
        else:
            response = None
    session.close()

    return response


async def get_breeds():
    """Get a list of breeds from an API request."""
    json_response = await fetch_json(API_URL + "breeds")
    if json_response is not None:
        return json_response["response"]["breeds"]
    else:
        return None


def make_breeds_list(breeds):
    """Return a string that holds a list of breeds."""
    return "Here's a list of available breeds.\n```\n" + "\n".join(breeds) + "```"
