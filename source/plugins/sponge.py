""""""
import re
from PIL import Image, ImageDraw, ImageFont

COMMAND = "spong"
TEMPLATE_FILE = "data/mocking_spongebob.jpg"
TEMPORARY_FILE = "/tmp/generated_image.jpg"
COMMAND_FORMAT = r"^!{0} (?P<rest>.*)$".format(COMMAND)
FONT_FILE = "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf"

FONT_SIZE = 128
LINE_WIDTH = 20
TEXT_SPACING = 40
VERTICAL_OFFSET = 30
BORDER_THICKNESS = 7
BORDER_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

async def command_sponge(client, message):
    """SpOnGeBoBiFiY a message."""

    # If the message doesn't fit the command syntax, then show the
    # help message.
    command_match = re.match(COMMAND_FORMAT, message.content, re.DOTALL)
    if command_match is None:
        await command_sponge_help(client, message)
        return
   
    # Get the top and bottom text from the raw text of the message.
    top_text, bottom_text = parse_text(command_match.group("rest"))

    # Create the meme and capture the file path.
    meme = generate_image(top_text, bottom_text)

    # Send the meme to the client.
    await client.send_file(message.channel, meme)


async def command_sponge_help(client, message):
    """"""
    print("help")


def parse_text(raw_text):
    """Parse two SpOnGeBoBeD lines out of raw text."""

    # Filter out non-alphanumeric/whitespace characters.
    char_filter = lambda char: char.isalnum() or char.isspace()
    characters = list(filter(char_filter, raw_text.lower()))

    # Turn all whitespace into simple spaces.
    normalize_space = lambda char: " " if char.isspace() else char
    characters = list(map(normalize_space, characters))

    # SpOnGeBoB the alphabetic characters.
    to_upper = False
    for index in range(len(characters)):
        if characters[index].isalpha():
            if to_upper:
                characters[index] = characters[index].upper()
                to_upper = False
            else:
                to_upper = True

    # Return two cut strings.
    return cut_text(characters)


def cut_text(characters):
    

    index = 0
    while index < LINE_WIDTH * 2:
        while index < LINE_WIDTH:
            if characters[index].isalpha():
                index += 1


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
    canvas = ImageDraw.Draw(image)
    meme_font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    image_width, image_height = image.size
    top_width, top_height = canvas.textsize(top_text, font=meme_font)
    bottom_width, bottom_height = canvas.textsize(bottom_text, font=meme_font)

    top_coordinates = ((image_width / 2) - (top_width / 2), VERTICAL_OFFSET)
    bottom_coordinates = ((image_width / 2) - (bottom_width / 2),
                          image_height - (VERTICAL_OFFSET * 1.5) - bottom_height)

    shifts = ((BORDER_THICKNESS, 0),
              (-BORDER_THICKNESS, 0),
              (0, BORDER_THICKNESS),
              (0, -BORDER_THICKNESS),
              (BORDER_THICKNESS, BORDER_THICKNESS),
              (-BORDER_THICKNESS, BORDER_THICKNESS),
              (BORDER_THICKNESS, -BORDER_THICKNESS),
              (-BORDER_THICKNESS, -BORDER_THICKNESS))

    for shift in shifts:
        shift_top_coordinates = (top_coordinates[0] + shift[0],
                                 top_coordinates[1] + shift[1])
        shift_bottom_coordinates = (bottom_coordinates[0] + shift[0],
                                    bottom_coordinates[1] + shift[1])
        canvas.text(shift_top_coordinates,
                    top_text,
                    font=meme_font,
                    fill=BORDER_COLOR,
                    spacing=TEXT_SPACING)
        canvas.text(shift_bottom_coordinates,
                    bottom_text,
                    font=meme_font,
                    fill=BORDER_COLOR,
                    spacing=TEXT_SPACING)

    canvas.text(top_coordinates, top_text, font=meme_font, fill=TEXT_COLOR, spacing=TEXT_SPACING)
    canvas.text(bottom_coordinates, bottom_text, font=meme_font, fill=TEXT_COLOR)

    image.save(TEMPORARY_FILE)

    return TEMPORARY_FILE
