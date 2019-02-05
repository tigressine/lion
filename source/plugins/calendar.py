"""Displays the current academic calendar information.

Written by eezstreet
"""

import discord
import re
import requests
from datetime import datetime

COMMAND = "calendar"
DEFAULT_TERM = "spring"
DEFAULT_YEAR = 2019
SYNTAX = "^!calendar ?(?P<term>[A-Za-z]+)? ?(?P<year>[0-9]+)? ?(?P<filter>[A-Za-z-_]+)?"
EMBED_COLOR = 0xFFFF00

async def fetch_calendar(term, year):
    """Fetch the calendar information for the given term and semester"""
    url = "http://calendar.ucf.edu/json/{}/{}".format(year, term)
    r = requests.get(url)
    return r.json()

async def command_calendar(client, message):
    """Show the academic calendar"""
    command_match = re.match(SYNTAX, message.content)

    if command_match is None:
        response = "Incorrect command syntax. Try `!help`."
        await message.channel.send(response)
        return

    term = command_match.group("term")
    if term is None:
        term = DEFAULT_TERM

    year = command_match.group("year")
    if year is None:
        year = DEFAULT_YEAR

    calendar_data = await fetch_calendar(term, year)
    if calendar_data['terms'] is None:
        await message.channel.send("Could not find data for that term.")
        return
    embed = generate_embed(calendar_data, command_match.group("filter"))

    await message.channel.send("", embed=embed)


def generate_embed(calendar_data, tags):
    embed = discord.Embed(color=EMBED_COLOR)
    
    term = calendar_data['terms'][0]
    for event in term['events']:
        if tags is None or event['tags'] is not None and tags in event['tags']:
            embed.add_field(name=event['category'], value=event['summary'], inline=False)
    return embed
