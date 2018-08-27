"""Generate a sassy SpOnGeBoB meme with a provided message.

Written by Tiger Sachse.
"""
import re
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

COMMAND = "spong"
TEMPORARY_FILE = "/tmp/generated_spongebob_meme.jpg"
TEMPLATE_FILE = "data/mocking_spongebob_template.jpg"
COMMAND_FORMAT = r"^!{0} (?P<rest>.*)$".format(COMMAND)
FONT_FILE = "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"

ODDS = .5
FONT_SIZE = 30
ODDS_OFFSET = .25
VERTICAL_OFFSET = 20
TEXT_COLOR = (0, 0, 0)
LINE_LENGTH_START = 30
REGION_COLOR = (255, 255, 255)
HORIZONTAL_OFFSET = VERTICAL_OFFSET

async def command_sponge(client, message):
    """SpOnGeIfY a message."""

    # If the message doesn't fit the command syntax or the message is not
    # all ASCII characters, then show the help message.
    command_match = re.match(COMMAND_FORMAT, message.content, re.DOTALL)
    if command_match is None or not is_ascii(command_match.group("rest")):
        await command_sponge_help(client, message)
        return

    # Get the normal and SpOnGe text from the raw text of the message.
    normal_text, sponge_text = generate_texts(message.author.display_name,
                                              command_match.group("rest"))

    # Create the meme and capture the file path.
    meme = generate_image(normal_text, sponge_text)

    # Send the meme to the client.
    await client.send_file(message.channel, meme)


async def command_sponge_help(client, message):
    """"""
    print("help")


def is_ascii(text):
    """Confirm that the given text is all ASCII characters."""
    return len(text) == len(text.encode())


def generate_texts(user, text):
    """Create the normal and SpOnGe text strings for the meme."""

    # Create a list of characters from the input text, and turn all
    # whitespace into regular spaces.
    characters = [" " if char.isspace() else char for char in text]

    # Force all characters to be lower case.
    characters = list(map(lambda char: char.lower(), characters))

    # Prepend the user's name to the front of the normal text if the user's
    # name is all ASCII.
    normal_text = "{0}: ".format(user) if is_ascii(user) else ""
    normal_text += text

    # SpOnGeIfY the alphabetic characters.
    last_upper = True
    for index in range(len(characters)):
        if characters[index].isalpha():

            # Calculate the odds that the character will be flipped to
            # upper case. This takes into account the previous character,
            # so long runs of upper/lower case characters are less likely.
            odds = ODDS - (ODDS_OFFSET if last_upper else -ODDS_OFFSET)
            if random.random() < odds:
                characters[index] = characters[index].upper()
                last_upper = True
            else:
                last_upper = False

    # Add the string "Me: " to the front of the SpOnGe text if the user's
    # name was all ASCII (so it matches the normal text). If the user's name
    # begins with a capital letter, capitalize "Me", else use a lower case "me".
    sponge_text = "{0}e: " if is_ascii(user) else ""
    sponge_text = sponge_text.format("m" if user[0].islower() else "M")

    # Add the actual SpOnGe text.
    sponge_text += "".join(characters)

    return normal_text, sponge_text


def wrap_text(text, canvas, width, font):
    """Wrap text based on its max width, given in pixels for a specific font."""

    # Start guessing at a certain constant character count.
    character_count = LINE_LENGTH_START
    usable_width = width - HORIZONTAL_OFFSET * 2

    # Use a loop to find the best break point for the text for the given width.
    # This is certainly not the most efficient way to do this.
    copied_text = textwrap.fill(text, width=character_count)
    while canvas.textsize(copied_text, font=font)[0] < usable_width:
        character_count += 1
        copied_text = textwrap.fill(text, width=character_count)

    # Return the text, wrapped to the appropriate length (minus one to
    # account for the extra iteration of the while loop).
    return textwrap.fill(text, width=character_count - 1)


def generate_image(normal_text, sponge_text):
    """Generate a meme with provided normal and SpOnGe text."""
    font = ImageFont.truetype(FONT_FILE, FONT_SIZE)

    # Open the template and set up a dummy canvas for measurements.
    template = Image.open(TEMPLATE_FILE)
    template_width, template_height = template.size
    test_canvas = ImageDraw.Draw(template)

    # Wrap the normal and SpOnGe text for the image.
    normal_text = wrap_text(normal_text, test_canvas, template_width, font)
    sponge_text = wrap_text(sponge_text, test_canvas, template_width, font)

    # The clearance is the space between the normal text and the SpOnGe text.
    clearance = test_canvas.textsize("A", font=font)[1] * 2
    normal_height = test_canvas.textsize(normal_text, font=font)[1]
    sponge_height = test_canvas.textsize(sponge_text, font=font)[1]

    # Calculate the height of the white text region above the template.
    text_region_height = (VERTICAL_OFFSET + normal_height +
                          clearance + sponge_height +
                          VERTICAL_OFFSET)

    # Create a new image with a white region above the template for text,
    # and prepare the canvas to draw the text.
    meme = template.crop((0, -text_region_height, template.width, template_height))

    # Fill the text region with the appropriate color.
    canvas = ImageDraw.Draw(meme)
    canvas.rectangle((0, 0, template_width, text_region_height), fill=REGION_COLOR)

    # Calculate the topleft coordinates for both strings of text.
    normal_coordinates = (HORIZONTAL_OFFSET, VERTICAL_OFFSET)
    sponge_coordinates = (HORIZONTAL_OFFSET,
                          VERTICAL_OFFSET + normal_height + clearance)

    # Draw the text onto the meme.
    canvas.text(normal_coordinates, normal_text, font=font, fill=TEXT_COLOR)
    canvas.text(sponge_coordinates, sponge_text, font=font, fill=TEXT_COLOR)

    meme.save(TEMPORARY_FILE)

    return TEMPORARY_FILE
