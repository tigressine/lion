"""Post a random corgi picture.

Written by Hayden Inghem and Joey the Corgi.
Revised by Tiger Sachse.
"""
import json
import random
import aiohttp
import discord

COMMAND = "corgi"
DEFAULT_IMAGE = "data/default_corgi.jpg"
TEMPORARY_FILE_FORMAT = "/tmp/random_corgi.{0}"
TUMBLR_KEY = "m9ZzEYfFoBEjEQpjqYunya8Ji2802GMj1ng1MWbKVY7Ra8kGEP"
BLOG_URL_FORMAT = "https://api.tumblr.com/v2/blog/{0}/posts/photo?api_key={1}"
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
    blog_url = BLOG_URL_FORMAT.format(random.choice(CORGI_BLOGS), TUMBLR_KEY)

    # First, attempt to retrieve a random corgi image URL from a blog.
    try:
        session = aiohttp.ClientSession() 

        async with session.get(blog_url) as url_response:
            if url_response.status == 200:
                image_url = get_random_image_url(await url_response.json())
            else:
                raise aiohttp.ClientResponseError(
                    "URL response status is not 200."
                )

        # Next, attempt to download that random image.
        async with session.get(image_url) as image_response:
            if image_response.status == 200:

                # Format the temporary file name with the file type
                # from the image URL.
                temporary_image = TEMPORARY_FILE_FORMAT.format(
                    image_url.rpartition(".")[2]
                )

                with open(temporary_image, "wb") as writable_file:
                    writable_file.write(await image_response.read())
            else:
                raise aiohttp.ClientResponseError(
                    "Image response status is not 200."
                )
        
        # Finally, send the image to the client.
        await client.send_file(message.channel, temporary_image)

    except Exception as exception:
        print(exception)
        await client.send_file(message.channel, DEFAULT_IMAGE)

    finally:
        session.close()


def get_random_image_url(data):
    """Get a random image URL from the data dictionaries."""
    random_post = random.choice(data["response"]["posts"])

    return random_post["photos"][0]["original_size"]["url"]
