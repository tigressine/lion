""""""
import re
import requests
from bs4 import BeautifulSoup

COMMAND = "gar"
PARSER = "html.parser"
CHOICE_PATTERN = r"(?P<choice>[ABCDHI]|(Libra))"
GARAGE_SINGLE_FORMAT = "{1} / {2} ({3}% full)"
GARAGE_LIST_FORMAT = "{0:>5}: {1:>4} / {2:>4} ({3:>2}% full)"
URL = "http://secure.parking.ucf.edu/GarageCount/iframe.aspx"
COMMAND_PATTERN = r"^!{0}( {1})?$".format(COMMAND, CHOICE_PATTERN)

class Garage:
    """"""
    def __init__(self, name, capacity):
        """"""
        self.name = name
        self.capacity = int(capacity)


    def set_available_space(self, available):
        """"""
        self.available = int(available)
        self.percent_full = self.__get_percent_full()


    def __get_percent_full(self):
        """"""
        percent_full = 100 - (self.available / self.capacity * 100)

        return int(percent_full) if percent_full >= 0 else 0

    
    def string(self, string_format=GARAGE_SINGLE_FORMAT):
            return string_format.format(self.name,
                                        self.available,
                                        self.capacity,
                                        self.percent_full)


async def command_garage_status(client, message):
    """"""
    command_match = re.match(COMMAND_PATTERN, message.content)

    if command_match is None:
        await command_garages_help(client, message)
        return
    
    garages = get_garages()
    if command_match.group("choice") is None:
        response = respond_all_garages(garages)
    else:
        for garage in garages:
            if garage.name == command_match.group("choice"):
                single_garage = garage
                break
        else:
            await command_garages_help(client, message)
            return

        response = respond_single_garage(single_garage)

    await client.send_message(message.channel, response)


async def command_garages_help(client, message):
    """"""
    pass


def respond_all_garages(garages):
    """"""
    response = "**Current garage availability on UCF campus:**```\n"
    response += garages[-1].string(string_format=GARAGE_LIST_FORMAT)
    response += "\n"
    for garage in garages[:-1]:
        response += garage.string(string_format=GARAGE_LIST_FORMAT)
        response += "\n"
    response += "```"

    return response


def respond_single_garage(garage):
    """"""
    response = "**Current availability of Garage {0}:**```\n".format(garage.name)
    response += garage.string(string_format=GARAGE_SINGLE_FORMAT)
    response += "\n```"

    return response


def get_garages():
    """"""
    garages = (
        Garage("A", 1623),
        Garage("B", 1259),
        Garage("C", 1852),
        Garage("D", 1241),
        Garage("H", 1284),
        Garage("I", 1231),
        Garage("Libra", 1007),
    )
    
    soup = BeautifulSoup(requests.get(URL).content, PARSER)
    available_spaces = (tag.get_text() for tag in soup.find_all("strong"))
  
    for available_space, garage in zip(available_spaces, garages):
        garage.set_available_space(available_space)
    
    return garages
