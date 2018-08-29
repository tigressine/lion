"""Garage status checker for Lion.

Scrapes the status of several garages on UCF campus from www.parking.ucf.edu.
Capable of displaying all garages or individual garages separately.

Written by Tiger Sachse.
Inspired by code written by Matthew Villegas.
"""
import re
import random
import discord
import requests
from bs4 import BeautifulSoup

ODDS = .05
VEHICLE_EMOJIS = ("🚗", "🚙", "🏎")

COMMAND = "garage"
PARSER = "html.parser"
CHOICE_PATTERN = r"(?P<choice>[ABCDHI]|(Libra))"
GARAGE_SINGLE_FORMAT = "{1} / {2} ({3}% full)"
GARAGE_LIST_FORMAT = "{0:>5}: {1:>4} / {2:>4} ({3:>2}% full)"
URL = "http://secure.parking.ucf.edu/GarageCount/iframe.aspx"
GARAGE_SINGLE_HEADER = "**Current availability of Garage {0}:**"
COMMAND_PATTERN = r"^!{0}( {1})?$".format(COMMAND, CHOICE_PATTERN)
GARAGE_LIST_HEADER = "**Current garage availability on UCF campus:**"

class Garage:
    """Hold various information about a UCF campus garage."""
    def __init__(self, name, capacity):
        """Initialize this garage with a name and capacity."""
        self.name = name
        self.capacity = int(capacity)


    def set_available_space(self, available_space):
        """Set the available space."""
        self.available_space = int(available_space)
        self.percent_full = self.__get_percent_full()


    def __get_percent_full(self):
        """Return the percentage of the garage that is full."""
        percent_full = 100 - (self.available_space / self.capacity * 100)

        return int(percent_full) if percent_full >= 0 else 0

    
    def string(self, string_format=GARAGE_SINGLE_FORMAT):
        """Return a formatted string containing this garage's information."""
        return string_format.format(self.name,
                                    self.available_space,
                                    self.capacity,
                                    self.percent_full)


async def command_garage_status(client, message):
    """Discover the status of garages on UCF campus."""
    command_match = re.match(COMMAND_PATTERN, message.content, re.IGNORECASE)

    # If the given command doesn't match the necessary pattern, call the
    # help function.
    if command_match is None:
        await command_garages_help(client, message)
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

    garage_message = await client.send_message(message.channel, response)

    # A little Easter egg. ;)
    if random.random() < ODDS:
        for emoji in VEHICLE_EMOJIS:
            await client.add_reaction(garage_message, emoji)


async def command_garages_help(client, message):
    """"""
    
    embed = discord.Embed(color=0xeee657)
    embed.add_field(name="Garage Status",
    value="This command allows you to check parking availability on UCF campus.")

    embed.add_field(name="Command",
                    value="!gar [garage]")

    embed.add_field(
        name="Examples",
        value="""```
        !garage A
            Show the availability of Garage A.
        !garage Libra
            Show the availability of Garage Libra.
        !garage
            Show the availability of all garages on campus.
        !garage help
            Show this help menu.
        ```""")
    await client.send_message(message.channel, embed=embed)


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
        garage.set_available_space(available_space)
    
    return garages
