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
SYNTAX_HELP = "Could not find data for that term. Try `!help` for syntax help."

async def fetch_calendar(term, year):
    """Fetch the calendar information for the given term and semester"""
    url = "http://calendar.ucf.edu/json/{}/{}".format(year, term)
    r = requests.get(url)
    return r.json()

async def command_calendar(client, message):
    """Show the academic calendar"""
    command_match = re.match(SYNTAX, message.content)

    if command_match is None:
        response = SYNTAX_HELP
        await message.channel.send(response)
        return

    term = command_match.group("term")
    if term is None:
        term = DEFAULT_TERM

    year = command_match.group("year")
    if year is None:
        year = DEFAULT_YEAR

    try:
        calendar_data = await fetch_calendar(term, year)
        if calendar_data['terms'] is None:
            await message.channel.send(SYNTAX_HELP)
            return
        embed = generate_embed(calendar_data, command_match.group("filter"))

        await message.channel.send("", embed=embed)
    except ValueError:
        await message.channel.send(SYNTAX_HELP)

def format_time(timestr):
    time = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%SZ')
    
    if time.hour is 0:
        return time.strftime('%B %e')
    return time.strftime('%b %e at %I:%M%p')

def generate_embed(calendar_data, tags):
    embed = discord.Embed(color=EMBED_COLOR)
    
    term = calendar_data['terms'][0]
    for event in term['events']:
        title = event['summary']

        if tags is None and event['tags'] is not None:
            title = "{} ({})".format(event['summary'], event['tags'][0])

        if tags is None or event['tags'] is not None and tags in event['tags']:
            if event['dtend'] is None or event['dtend'] is '':
                """There is no ending date to be considered."""
                embed.add_field(name=title, value=format_time(event['dtstart']), inline=False)
            else:
                embed.add_field(name=title, value="{} to {}".format(format_time(event['dtstart']), format_time(event['dtend'])), inline=False)
    return embed
