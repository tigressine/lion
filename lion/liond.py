"""Create and run a Discord bot.

This bot will load every cog (plugin) in the cogs directory, and then will
run continously until interrupted. This script should be run as a daemon.

Written by Tiger Sachse.
"""
import json
import logging
import settings
import utilities
from pathlib import Path
from discord.ext import commands


class LionBot(commands.Bot):
    """"""

    def __init__(self, guild_settings_file, *arguments, **keyword_arguments):
        """"""
        super().__init__(*arguments, **keyword_arguments)

        self.guild_settings_file = guild_settings_file
        try:
            with open(self.guild_settings_file, "r") as open_guild_settings_file:
                self.guild_settings = json.load(open_guild_settings_file)
        except FileNotFoundError:
            self.guild_settings = {}

    def write_guild_settings(self):
        """"""
        with open(self.guild_settings_file, "w") as open_guild_settings_file:
            json.dump(open_guild_settings_file, self.guild_settings)


    def get_guild_settings(self, guild_id):
        return self.guild_settings[str(guild_id)]
    '''
    def log(self, message, level=logging.INFO):
        pass
    '''


def load_cogs(bot, cogs_directory):
    """Load all cogs within a cogs directory into a bot."""
    LOG_MESSAGE_FORMAT = "Attempting to load '{0}' cog: {1}"

    cogs_loaded = 0
    cogs_path = Path(cogs_directory)
    for cog in (path.stem for path in cogs_path.iterdir()):
        try:
            bot.load_extension(".".join((cogs_directory, str(cog), str(cog))))
            utilities.log(LOG_MESSAGE_FORMAT.format(cog, " Success!"),
                          level=logging.INFO)
            cogs_loaded += 1
        except ModuleNotFoundError:
            utilities.log(LOG_MESSAGE_FORMAT.format(cog, " Failure!"),
                          level=logging.WARNING)

    loaded_message = "Loaded {0} cog{1}.".format(cogs_loaded,
                                                 "s" if cogs_loaded != 1 else "")
    utilities.log(loaded_message, level=logging.INFO)


# Main entry point to the daemon.
utilities.log("Initializing Lion...", level=logging.INFO)
bot = LionBot(settings.GUILD_SETTINGS_PATH, command_prefix=settings.PREFIX)
load_cogs(bot, settings.COGS_DIRECTORY)
utilities.log("Starting Lion...", level=logging.INFO)
bot.run(utilities.load_token(settings.TOKEN_PATH))
