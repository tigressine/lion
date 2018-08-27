""""""
import re
import random
from PIL import Image, ImageDraw, ImageFont

ODDS = .5
ODDS_OFFSET = .25
COMMAND = "spong"
TEMPLATE_FILE = "data/mocking_spongebob_twitter.jpg"
TEMPORARY_FILE = "/tmp/generated_image.jpg"
COMMAND_FORMAT = r"^!{0} (?P<rest>.*)$".format(COMMAND)
FONT_FILE = "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"

FONT_SIZE = 30
VERTICAL_OFFSET = 15
HORIZONTAL_OFFSET = VERTICAL_OFFSET
TEXT_COLOR = (0, 0, 0)

async def command_sponge(client, message):
    """SpOnGeBoBiFiY a message."""

    # If the message doesn't fit the command syntax, then show the
    # help message.
    command_match = re.match(COMMAND_FORMAT, message.content, re.DOTALL)
    if command_match is None:
        await command_sponge_help(client, message)
        return
   
    # Get the top and bottom text from the raw text of the message.
    #normal_text, sponge_text = parse_text(command_match.group("rest"))
    normal_text, sponge_text = generate_texts(message.author.name,
                                              command_match.group("rest"))

    # Create the meme and capture the file path.
    meme = generate_image(normal_text, sponge_text)

    # Send the meme to the client.
    await client.send_file(message.channel, meme)


async def command_sponge_help(client, message):
    """"""
    print("help")


def generate_texts(user, text):
    characters = [" " if char.isspace() else char for char in text]
    normal_text = "{0}: {1}".format(user, text)

    # SpOnGeBoB the alphabetic characters.
    last_upper = True
    for index in range(len(characters)):
        if characters[index].isalpha():
            odds = ODDS + (ODDS_OFFSET if last_upper else -ODDS_OFFSET)
            if random.random() > odds:
                characters[index] = characters[index].upper()
                last_upper = True
            else:
                last_upper = False

    sponge_text = "{0}e: {1}".format("m" if characters[0].islower() else "M",
                                     "".join(characters))

    return normal_text, sponge_text


def generate_image(normal_text, sponge_text):
    """"""
    image = Image.open(TEMPLATE_FILE)
    canvas = ImageDraw.Draw(image)
    meme_font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    image_width, image_height = image.size
    normal_width, normal_height = canvas.textsize(normal_text, font=meme_font)
    sponge_width, sponge_height = canvas.textsize(sponge_text, font=meme_font)

    top_coordinates = (HORIZONTAL_OFFSET, VERTICAL_OFFSET)
    bottom_coordinates = (HORIZONTAL_OFFSET,
                          VERTICAL_OFFSET + normal_height * 2 + VERTICAL_OFFSET)

    canvas.text(top_coordinates, normal_text, font=meme_font, fill=TEXT_COLOR)
    canvas.text(bottom_coordinates, sponge_text, font=meme_font, fill=TEXT_COLOR)

    image.save(TEMPORARY_FILE)

    return TEMPORARY_FILE
