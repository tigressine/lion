"""Garage status checker for Lion.

Scrapes the status of several garages on UCF campus from www.parking.ucf.edu.
Capable of displaying all garages or individual garages separately.

Written by Tiger Sachse.
Inspired by code written by Matthew Villegas.
"""
import re
import random
import requests
from bs4 import BeautifulSoup

ODDS = .05
VEHICLE_EMOJIS = ("🚗", "🚙", "🏎")

COMMAND = "garage"
PARSER = "html.parser"
GARAGE_SINGLE_FORMAT = "{1} / {2} ({3}% full)"
CHOICE_PATTERN = r"(?P<choice>[ABCDHI]|(Libra))"
GARAGE_LIST_FORMAT = "{0:>5}: {1:>4} / {2:>4} ({3:>2}% full)"
URL = "http://secure.parking.ucf.edu/GarageCount/iframe.aspx"
GARAGE_SINGLE_HEADER = "**Current saturation of Garage {0}:**"
COMMAND_PATTERN = r"^!{0}( {1})?$".format(COMMAND, CHOICE_PATTERN)
GARAGE_LIST_HEADER = "**Current garage saturation on UCF campus:**"

class Garage:
    """Hold various information about a UCF campus garage."""
    def __init__(self, name, capacity):
        """Initialize this garage with a name and capacity."""
        self.name = name
        self.capacity = int(capacity)


    def __get_percent_full(self):
        """Return the percentage of the garage that is full."""
        percent_full = self.saturated_space / self.capacity * 100

        return int(percent_full) if percent_full >= 0 else 0


    def set_saturated_space(self, available_space):
        """Set the saturated space."""
        self.saturated_space = max(self.capacity - int(available_space), 0)
        self.percent_full = self.__get_percent_full()


    def string(self, string_format=GARAGE_SINGLE_FORMAT):
        """Return a formatted string containing this garage's information."""
        return string_format.format(
            self.name,
            self.saturated_space,
            self.capacity,
            self.percent_full
        )


async def command_garage_status(client, message):
    """Discover the status of garages on UCF campus."""
    command_match = re.match(COMMAND_PATTERN, message.content, re.IGNORECASE)

    # If the given command doesn't match the necessary pattern, we've got a problem.
    if command_match is None:
        response = "You've got the garage syntax wrong. Try `!help`."
        await message.channel.send(response)

        return

    garages = get_garages()

    # If no garage is selected, then respond with all garages.
    if command_match.group("choice") is None:
        response = respond_with_all_garages(garages)

    # Else respond with a specific garage's information.
    else:
        for garage in garages:
            if re.match(garage.name, command_match.group("choice"), re.IGNORECASE):
                response = respond_with_single_garage(garage)
                break

    garage_message = await message.channel.send(response)

    # A little Easter egg. ;)
    if random.random() < ODDS:
        for emoji in VEHICLE_EMOJIS:
            await garage_message.add_reaction(emoji)


def respond_with_all_garages(garages):
    """Generate a response for all garages."""
    response = GARAGE_LIST_HEADER + "```\n"

    # The Libra Garage is always at the bottom of the garages tuple, but it
    # looks better at the top of the response. Add the Libra Garage to the
    # response first.
    response += garages[-1].string(string_format=GARAGE_LIST_FORMAT)
    response += "\n"

    # Add the rest of the garages to the response.
    for garage in garages[:-1]:
        response += garage.string(string_format=GARAGE_LIST_FORMAT)
        response += "\n"
    response += "```"

    return response


def respond_with_single_garage(garage):
    """Generate a response for a single garage."""
    response = GARAGE_SINGLE_HEADER.format(garage.name) + "```\n"
    response += garage.string(string_format=GARAGE_SINGLE_FORMAT)
    response += "\n```"

    return response


def get_garages():
    """Scrape all the garages from the Internet!"""

    # Create a list of garages with their names and capacities. I hardcoded
    # the capacities because it means less scraping, and the capacities of
    # physical parking garages certainly won't be changing any time soon.
    garages = (
        Garage("A", 1623),
        Garage("B", 1259),
        Garage("C", 1852),
        Garage("D", 1241),
        Garage("H", 1284),
        Garage("I", 1231),
        Garage("Libra", 1007),
    )

    # Brew up some beautiful HTML soup.
    soup = BeautifulSoup(requests.get(URL).content, PARSER)

    # Create a generator that produces the text for each "strong" tag in the
    # beautiful HTML soup. The "strong" tags for this particular HTML hold
    # the counts of unused spaces for each garage. The tags are in the same
    # order as the garages in garages.
    available_spaces = (tag.get_text() for tag in soup.find_all("strong"))

    # Iterate through the available spaces generator and the tuple of garages,
    # setting each garage with the appropriate amount of available space
    # along the way.
    for available_space, garage in zip(available_spaces, garages):
        garage.set_saturated_space(available_space)

    return garages
