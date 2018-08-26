""""""
import re
from PIL import Image, ImageDraw, ImageFont

COMMAND = "spong"
TEMPLATE_FILE = "data/mocking_spongebob.jpg"
TEMPORARY_FILE = "/tmp/generated_image.jpg"
FONT_FILE = "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf"
FONT_SIZE = 128
LINE_WIDTH = 20
TEXT_COLOR = (255, 255, 255)
TOP_LEFT_COORDS = (10, 10)
BOTTOM_LEFT_COORDS = (10, 500)
COMMAND_FORMAT = r"^!{0} (?P<rest>.*)$".format(COMMAND)

async def command_sponge(client, message):
    """"""
    command_match = re.match(COMMAND_FORMAT, message.content, re.DOTALL)
    if command_match is None:
        await command_sponge_help(client, message)
        return
    
    top_text, bottom_text = parse_text(command_match.group("rest"))
    generate_image(top_text, bottom_text)

    await client.send_file(message.channel, TEMPORARY_FILE)


async def command_sponge_help(client, message):
    """"""
    print("help")

def parse_text(raw_text):
    """"""

    # Filter out non-alphanumeric/whitespace characters.
    char_filter = lambda char: char.isalnum() or char.isspace()
    characters = list(filter(char_filter, raw_text.lower()))

    # Turn all whitespace into simple spaces.
    normalize_space = lambda char: " " if char.isspace() else char
    characters = list(map(normalize_space, characters))

    # SpOnGeBoB the alphabetic characters.
    to_upper = True
    for index in range(len(characters)):
        if characters[index].isalpha():
            if to_upper is True:
                characters[index] = characters[index].upper()
                to_upper = False
            else:
                to_upper = True

    # Cut the text into a top and bottom line.
    if len(characters) > LINE_WIDTH * 2:
        top_text = "".join(characters[:LINE_WIDTH])
        bottom_text = "".join(characters[LINE_WIDTH: LINE_WIDTH * 2])
    elif len(characters) > LINE_WIDTH:
        top_text = "".join(characters[:LINE_WIDTH])
        bottom_text = "".join(characters[LINE_WIDTH:])
    else:
        top_text = "".join(characters)
        bottom_text = ""

    return top_text, bottom_text


def generate_image(top_text, bottom_text):
    """"""
    image = Image.open(TEMPLATE_FILE)
    draw = ImageDraw.Draw(image)
    
    meme_font = ImageFont.truetype(FONT_FILE, FONT_SIZE)
    draw.text(TOP_LEFT_COORDS, top_text, font=meme_font, fill=TEXT_COLOR)
    draw.text(BOTTOM_LEFT_COORDS, bottom_text, font=meme_font, fill=TEXT_COLOR)

    image.save(TEMPORARY_FILE)
