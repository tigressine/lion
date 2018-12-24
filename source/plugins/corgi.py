"""Post a random corgi picture.

Written by Hayden Inghem and Joey the Corgi.
Heavily revised by Tiger Sachse.
"""
import json
import random
import aiohttp
import discord

COMMAND = "corgi"
MAX_ATTEMPTS = 20
DEFAULT_IMAGE = "data/default_corgi.jpg"
TEMPORARY_FILE_FORMAT = "/tmp/random_corgi.{0}"
TUMBLR_KEY = "m9ZzEYfFoBEjEQpjqYunya8Ji2802GMj1ng1MWbKVY7Ra8kGEP"
BLOG_URL_FORMAT = "https://api.tumblr.com/v2/blog/{0}/posts/photo?api_key={1}"
CORGI_BLOGS = (
    "corgito",
    "acorgiaday",
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

    # If something goes wrong, send a default corgi to the client.
    except Exception as exception:
        await client.send_file(message.channel, DEFAULT_IMAGE)

    finally:
        session.close()


def get_random_image_url(data):
    """Get a random image URL out of the provided data."""
   
    # Get a new post from the data. Occasionally the chosen post won't include
    # any pictures. If this happens, the code will try new posts a certain
    # number of times until a picture is found.
    attempts = 1
    random_post = random.choice(data["response"]["posts"])
    while("photos" not in random_post and attempts < MAX_ATTEMPTS):
        random_post = random.choice(data["response"]["posts"])
        attempts += 1
        print(attempts)

    # If no picture is found after all those attempts, throw an error.
    # Otherwise, return the URL of the picture in the post.
    if "photos" not in random_post:
        raise aiohttp.ClientResponseError(
            "No pictures found after {0} attempts.".format(attempts)
        )
    else:
        return random_post["photos"][0]["original_size"]["url"]
