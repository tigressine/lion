"""Shows the current weather conditions along with a forecast
Can choose the city or zip code, defaults to Orlando if neither provided
Uses the OpenWeatherMaps API - openweathermap.org

Written by Sam Shannon
"""

import re
import discord
import requests
import time
import math
from datetime import datetime

COMMAND = "weather"
COMMAND_FORMAT = r"^!{0}( ((?P<location>[a-zA-Z ]+|\d{{5}})))?$".format(COMMAND)

API_URL = "https://api.openweathermap.org/data/2.5/"
API_KEY_FILE = "data/weather_token.txt"

DEFAULT_LOCATION = "Orlando"
EMBED_COLOR = 0xffee05
LARGE_ICONS = True
ICON_SIZE = 128 if LARGE_ICONS else 64
FORECAST_NUM = 3

DEBUG = False       # prints api urls to console

with open(API_KEY_FILE, "r") as f:
    API_KEY = f.read()[:-1]
API_OPTS = "&units=imperial&apikey={}".format(API_KEY)


async def command_weather(client, message):
    """Show the weather"""
    command_match = re.match(COMMAND_FORMAT, message.content)
    
    # check syntax
    if command_match is None:
        response = "Incorrect command syntax. Try `!help`."
        await client.send_message(message.channel, response)
        return
    
    # get location from command
    location = command_match.group("location")
    if location is None:
        location = DEFAULT_LOCATION
    
    weather_data = await fetch_weather("weather", location)
    
    # check for api error response
    if weather_data['cod'] != 200:
        err_message = weather_data['message'] if 'message' in weather_data else "unknown"
        response = "**API Error: {}**".format(err_message)
        await client.send_message(message.channel, response)
        return
    
    forecast_data = await fetch_weather("forecast", location)
    embed = generate_embed(weather_data, forecast_data)

    await client.send_message(message.channel, "", embed=embed)
    

async def fetch_weather(type, location):
    """Fetch the current weather or a forecast for a location"""
    try:
        int(location)
        key = "zip"     # using zip code
    except ValueError:
        key = "q"       # using city name
        
    url = "{}{}?{}={}{}".format(API_URL, type, key, location, API_OPTS)
    if DEBUG:
        print(url)
    r = requests.get(url)
    return r.json()

    
def f_to_c(temp):
    """Convert farenheit to celsius"""
    return (temp-32)*5/9
    
    
def generate_embed(wdata, fdata):
    """Generate the rich embed to display"""
    embed = discord.Embed(color=EMBED_COLOR)
    
    country = wdata['sys']['country'].lower()
    title = "{} :flag_{}:".format(wdata['name'], country)
    
    # footer & timestamp
    dt_diff_mins = math.ceil((time.time() - int(wdata['dt']))/60)
    last_up_s = "s" if dt_diff_mins > 1 else ""
    embed.set_footer(text="Last updated {} minute{} ago".format(dt_diff_mins, last_up_s))
    embed.timestamp = datetime.utcfromtimestamp(wdata['dt'])
    
    weather_id = wdata['weather'][0]['id']
    temp_f = wdata['main']['temp']
    wind_speed = wdata['wind']['speed']
    
    # set the thumbnail
    weather_icon_url = "https://www.gstatic.cn/onebox/weather/{}/{}.png".format(ICON_SIZE, get_weather_icon(weather_id))
    embed.set_thumbnail(url=weather_icon_url)
    
    # using a field for the title/description as
    # emojis don't work in titles on mobile
    desc = ""
    desc += "{}".format(get_temp_comment(weather_id, temp_f))
    wind_comment = get_wind_comment(wind_speed)
    if wind_comment:
        desc += "\n{}".format(wind_comment)
    embed.add_field(
        name = title,
        value = desc + "\n​",
        inline = False
    )
    
    temp_c = f_to_c(temp_f)
    embed.add_field(
        name="Temperature",
        value="🌡 {}°F ({}°C)".format(roundtoint(temp_f), roundtoint(temp_c)),
        inline=True
    )
    
    embed.add_field(
        name="Description",
        value="📢 {}".format(wdata['weather'][0]['description'].capitalize()),
        inline=True
    )
    
    # 1h rain not available for some locations
    # falls back on the 3h
    rain_str = "last hour"
    if 'rain' in wdata:
        if '1h' in wdata['rain']:
            rain = wdata['rain']['1h']
        else:
            rain = wdata['rain']['3h']
            rain_str = "last 3 hours"
    else:
        rain = "0"
    embed.add_field(
        name="Rainfall",
        value="🌧️ {}mm in {}".format(rain, rain_str),
        inline=True
    )
    
    embed.add_field(
        name="Cloud cover",
        value="☁️ {}%".format(wdata['clouds']['all']),
        inline=True
    )
    
    wind_dir = wdata['wind']['deg'] if 'deg' in wdata['wind'] else -1
    embed.add_field(
        name="Wind",
        value="💨 {}mph {}".format(roundtoint(wind_speed), get_wind_arrow(wind_dir), wind_dir),
        inline=True
    )
    
    embed.add_field(
        name="Humidity",
        value="💦 {}%".format(wdata['main']['humidity']),
        inline=True
    )
    
    # spacer, using unicode zero width spaces
    embed.add_field(
        name="​",
        value="​",
        inline=False
    )
    
    # forecast section
    forecast = generate_forecast(fdata)
    embed.add_field(
        name="\n\nForecast",
        value=forecast,
        inline=False
    )
    
    return embed
    
    
def get_weather_icon(wid):
    """Get a google weather icon name for the corresponding weather type id
    
    Used for the thumbnail.
    See: https://openweathermap.org/weather-conditions
    """

    if wid >= 800:
        if wid == 800: return "sunny"
        elif wid == 801: return "sunny_s_cloudy"
        elif wid == 802: return "partly_cloudy"
        else: return "cloudy"
    
    if wid >= 700:
        if wid == 701: return "mist"
        else: return "fog"
        
    if wid >= 600:
        if wid == 600: return "snow_light"
        elif wid < 611: return "snow"
        elif wid == 611: return "sleet"
        else: return "snow_s_rain"
        
    if wid >= 500:
        if wid == 500: return "rain_light"
        elif wid == 501: return "rain"
        elif wid < 511: return "rain_heavy"
        else: return "sunny_s_rain"
        
    if wid >= 300:
        return "sunny_s_rain"
        
    if wid >= 200:
        return "thunderstorms"
        
    return None
    
    
def get_weather_emoji(wid):
    """Get a weather emoji for the corresponding weather type id
    
    Used for the forecast.
    See: https://openweathermap.org/weather-conditions
    """

    if wid >= 800:
        if wid == 800: return "☀️"
        elif wid == 801: return "🌤️"
        elif wid == 802: return "⛅"
        elif wid == 803: return "🌥️"
        else: return "☁️"
        
    if wid >= 700:
        if wid == 781: return "🌪️"
        else: return "🌫️"
        
    if wid >= 600:
        return "🌨️"
        
    if wid >= 500:
        if wid < 520: return "🌧️"
        else: return "🌦️"
        
    if wid >= 300:
        return "🌦️"
        
    if wid >= 200:
        if wid < 210 or wid >= 230: return "⛈️"
        else: return "🌩️"
        
    return ""
    

def get_wind_arrow(wdir):
    """Gets an arrow emoji representing the given wind direction"""

    if wdir == -1:
        return ""
    
    if wdir > 337.5 or wdir <= 22.5:
        return ":arrow_down:"
        
    elif wdir <= 67.5:
        return ":arrow_lower_left:"
        
    elif wdir <= 112.5:
        return ":arrow_left:"
        
    elif wdir <= 157.5:
        return ":arrow_upper_left:"
        
    elif wdir <= 202.5:
        return ":arrow_up:"
        
    elif wdir <= 247.5:
        return ":arrow_upper_right:"
        
    elif wdir <= 292.5:
        return ":arrow_right:"
        
    else:
        return ":arrow_lower_right:"
        
        
def get_temp_comment(wid, temp):
    """Gets a comment about the current temperature"""
    temp = roundtoint(temp)
    
    # when over 80 degrees and not cloudy
    if temp >= 80 and (wid == 800 or wid == 801):
        return "Suns out guns out 💪😎"
        
    else:
        if temp >= 100: return "It's a right scorcher 🔥"
        elif temp >= 90: return "It's pretty hot out 🌞"
        elif temp >= 80: return "It's a little hot 🌞"
        elif temp >= 70: return "It's comfortably warm 👌"
        elif temp >= 60: return "It might be a bit chilly"
        elif temp >= 42: return "It's cold - don't forget your jacket"
        elif temp >= 32: return "Almost freezing - wrap up warm"
        else: return "It's below freezing! ❄️"
        

def get_wind_comment(wspeed):
    """Gets a comment about the current wind speed"""
    
    if wspeed > 50: return "⚠️ Dangerously high wind level"
    elif wspeed > 40: return "It is extremely windy"
    elif wspeed > 30: return "It is very windy"
    elif wspeed > 24: return "It is fairly windy"
    elif wspeed > 18: return "It is a little windy"
    elif wspeed > 12: return "There is a moderate breeze"
    elif wspeed > 7: return "There is a gentle breeze"
    elif wspeed > 3: return "There is a light breeze"
    else: return None
        
        
def generate_forecast(fdata):
    """Generates a human readable forecast from the forecast data"""

    output = ""
    x = 0
    xc = 0
    while xc < FORECAST_NUM:
        # get weather data for a time
        tdata = fdata['list'][x]
        timestamp = tdata['dt']
        hours = roundtoint((timestamp - time.time()) / 3600)
        
        # only use forecast times more than 30 mins from now
        if hours > 0:
            strf = datetime.fromtimestamp(timestamp).strftime('%I %p').lstrip("0").lower()
            weather_id = tdata['weather'][0]['id']
            output += "**{} hours ({})**".format(hours, strf)
            
            output += ": {} °F".format(roundtoint(tdata['main']['temp']))
            output += "   -   {} {}".format(get_weather_emoji(weather_id), tdata['weather'][0]['description'].capitalize())
            output += "\n"
            
            xc += 1
        x += 1
    
    return output
    
    
def roundtoint(x):
    """Rounds number to nearest integer"""
    return int(round(x))
    
