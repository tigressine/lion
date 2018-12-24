"""
Written by Hayden Inghem and Joey The corgi 
"""
import discord
import aiohttp
import random
import json

COMMAND = "corgi"

# tumblr key
key = "m9ZzEYfFoBEjEQpjqYunya8Ji2802GMj1ng1MWbKVY7Ra8kGEP"

# If u have anymore strictly corgi blogs pls add

corgi_blogs = [
        "corgioverload",
        "acorgiaday",
        "omelettethecorgi",
        "discothecorgi",
        "worldofcorgi",
        "corgito",
        "vegasthecorgi"
        ]



async def command_corgi(client,message):
    try:
        session = aiohttp.ClientSession()
        random_element = random.randrange(0, len(corgi_blogs))
        async with session.get("https://api.tumblr.com/v2/blog/" + corgi_blogs[random_element] + "/posts/photo?api_key=" + key) as r:
            if r.status == 200:
                response = await r.read()
                data = json.loads(response)
                random_picture = random.randrange(0, 20)
                image_url = data['response']['posts'][random_picture]['photos'][0]['original_size']['url']
            await client.send_message(message.channel, image_url)
            session.close()
    except Exception as e:
        session.close()
        print("Exception: %s" % e)
        await command_corgi(client,message)







