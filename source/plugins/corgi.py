"""Post a random corgi picture.

Written by Hayden Inghem and Joey the Corgi.
Revised by Tiger Sachse.
"""
import json
import random
#import aiohttp
import discord
import requests

COMMAND = "corgi"
TUMBLR_KEY = "m9ZzEYfFoBEjEQpjqYunya8Ji2802GMj1ng1MWbKVY7Ra8kGEP"
TEMPORARY_FILE_FORMAT = "/tmp/random_corgi.{0}"
CORGI_BLOGS = (
    "corgito",
    "acorgiaday",
    "worldofcorgi",
    "corgioverload",
    "vegasthecorgi",
    "discothecorgi",
    "omelettethecorgi",
)

async def command_corgi(client, message):
    """Fetch a corgi picture from Tumblr and post it."""
    blog_url = (
        "https://api.tumblr.com/v2/blog/"
        + random.choice(CORGI_BLOGS)
        + "/posts/photo?api_key="
        + TUMBLR_KEY
    )

    # First, attempt to retrieve a random corgi image URL from one of the blogs.
    try:
        image_url_request = requests.get(blog_url)
        if image_url_request.status_code == 200:
            image_url = get_random_image_url(image_url_request.json())
        else:
            raise requests.RequestException("URL request status was not 200.")

        # Next, attempt to download that random image.
        image_request = requests.get(image_url)
        if image_request.status_code == 200:
            with open(TEMPORARY_FILE, "wb") as writable_file:
                writable_file.write(image_request.content)
        else:
            raise requests.RequestException("Image request status was not 200.")

        # 

        # Finally, send the image to the client.
        await client.send_file(message.channel, TEMPORARY_FILE)

    except Exception as exception:
        print(exception)
        await client.send_message(message.channel, "Something wen't wrong!")


def get_random_image_url(data):
    """Get a random image URL from the data dictionaries."""
    random_post = random.choice(data["response"]["posts"])

    return random_post["photos"][0]["original_size"]["url"]
