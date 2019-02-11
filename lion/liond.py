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
from systemd.journal import JournalHandler


class LionBot(commands.Bot):
    """"""
    def __init__(self,
                 guild_settings_file,
                 cogs_directory,
                 *arguments,
                 **keyword_arguments):
        """"""
        super().__init__(*arguments, **keyword_arguments)

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(JournalHandler())
        self._logger.setLevel(logging.INFO)

        self.load_cogs(cogs_directory)

        self._guild_settings_file = guild_settings_file
        try:
            with open(self._guild_settings_file, "r") as open_guild_settings_file:
                self._guild_settings = json.load(open_guild_settings_file)
        except FileNotFoundError:
            self._guild_settings = {}

    def write_guild_settings(self):
        """"""
        with open(self._guild_settings_file, "w") as open_guild_settings_file:
            json.dump(open_guild_settings_file, self._guild_settings)

    def get_guild_settings(self, guild_id):
        """"""
        guild_id = str(guild_id)
        if guild_id in self._guild_settings:
            return self._guild_settings[guild_id]
        else:
            return None
    
    def log(self, message, level=logging.INFO):
        """"""
        self._logger.log(level, message)

    def load_cogs(self, cogs_directory):
        """Load all cogs within the cogs directory into the bot."""
        LOG_MESSAGE_FORMAT = "Attempting to load '{0}' cog: {1}"

        cogs_loaded = 0
        cogs_directory = Path(cogs_directory)
        for cog in (path.stem for path in cogs_directory.iterdir()):
            try:
                self.load_extension(".".join((str(cogs_directory),
                                              str(cog),
                                              str(cog))))
                self.log(LOG_MESSAGE_FORMAT.format(cog, " Success!"),
                         level=logging.INFO)
                cogs_loaded += 1
            except ModuleNotFoundError:
                self.log(LOG_MESSAGE_FORMAT.format(cog, " Failure!"),
                         level=logging.WARNING)

        log_message = "Loaded {0} cog{1}.".format(cogs_loaded,
                                                  "s" if cogs_loaded != 1 else "")
        self.log(log_message, level=logging.INFO)


# Main entry point to the daemon.
bot = LionBot(settings.GUILD_SETTINGS_PATH,
              settings.COGS_DIRECTORY,
              command_prefix=settings.PREFIX)
bot.log("Starting Lion...", level=logging.INFO)
bot.run(utilities.load_token(settings.TOKEN_PATH))
