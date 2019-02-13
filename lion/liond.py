"""Create and run a Discord bot.

This bot will load every cog (plugin) in the enabled cogs directory, and then
will run continously until interrupted. This script should be run as a daemon.

Written by Tiger Sachse.
"""
import json
import shutil
import logging
import discord
import settings
import utilities
from pathlib import Path
from discord.ext import commands
from systemd.journal import JournalHandler


class LionBot(commands.Bot):
    """A custom child class of the discord.py API's built-in Bot class.

    This class maintains a logger and a dictionary of guild-specific settings.
    """
    def __init__(self,
                 guild_settings_file,
                 enabled_cogs_directory,
                 *arguments,
                 **keyword_arguments):
        """Initialize the bot with a logger and a dictionary of guild settings."""
        super().__init__(*arguments, **keyword_arguments)

        # Create a new logger.
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(JournalHandler())
        self._logger.setLevel(logging.INFO)

        # Remove the default help command.
        self.remove_command("help")

        # Load all cogs in the enabled cogs directory.
        self.load_cogs(enabled_cogs_directory)

        # Load the guild settings from the guild settings file. If the file
        # doesn't exist, create a new empty dictionary.
        self._guild_settings_file = guild_settings_file
        try:
            with open(self._guild_settings_file, "r") as open_guild_settings_file:
                self._guild_settings = json.load(open_guild_settings_file)
        except FileNotFoundError:
            self._guild_settings = {}

    def load_cogs(self, enabled_cogs_directory):
        """Load all cogs within the enabled cogs directory into the bot."""
        LOG_MESSAGE_FORMAT = "Attempting to load '{0}' cog: {1}"

        cogs_loaded = 0
        enabled_cogs_directory = Path(enabled_cogs_directory)
        for cog in (path.stem for path in enabled_cogs_directory.iterdir()):
            try:
                self.load_extension(".".join((str(enabled_cogs_directory),
                                              str(cog),
                                              str(cog))))
                self.log(LOG_MESSAGE_FORMAT.format(cog, " Success!"),
                         level=logging.INFO)
                cogs_loaded += 1
            except (ModuleNotFoundError, discord.errors.ClientException):
                self.log(LOG_MESSAGE_FORMAT.format(cog, " Failure!"),
                         level=logging.WARNING)

        log_message = "Loaded {0} cog{1}.".format(cogs_loaded,
                                                  "s" if cogs_loaded != 1 else "")
        self.log(log_message, level=logging.INFO)

    def write_guild_settings(self):
        """Backup any old guild settings and write the current ones to disk."""
        shutil.copy2(self._guild_settings_file,
                     self._guild_settings_file + ".backup")

        with open(self._guild_settings_file, "w") as open_guild_settings_file:
            json.dump(self._guild_settings, open_guild_settings_file)

    def get_guild_settings(self, guild_id):
        """Get a particular guild's settings, based on the guild id."""
        guild_id = str(guild_id)
        if guild_id in self._guild_settings:
            return self._guild_settings[guild_id]
        else:
            return None

    def set_guild_setting(self, guild_id, setting, value):
        """Set a guild setting for a particular guild id."""
        guild_id = str(guild_id)
        if guild_id not in self._guild_settings:
            self._guild_settings[guild_id] = {}
        self._guild_settings[guild_id][setting] = value
        self.write_guild_settings()
    
    def log(self, message, level=logging.INFO):
        """Log a message using the bot's logger."""
        self._logger.log(level, message)


# Main entry point to the daemon.
bot = LionBot(settings.GUILD_SETTINGS_PATH,
              settings.ENABLED_COGS_DIRECTORY,
              command_prefix=settings.PREFIX)
bot.log("Starting Lion...", level=logging.INFO)
bot.run(utilities.load_token(settings.TOKEN_PATH))
