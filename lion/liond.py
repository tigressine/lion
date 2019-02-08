"""Load all cogs into the main bot and run the bot.

Written by Tiger Sachse.
"""
import settings
import utilities
from pathlib import Path
from discord.ext import commands


def load_cogs(bot, cogs_directory):
    """Load all cogs into a bot within a cogs directory."""
    cogs_loaded = 0
    cogs_path = Path(cogs_directory)

    for cog in (path.stem for path in cogs_path.iterdir()):
        print("Attempting to load '{0}' cog:".format(cog), end="")
        
        try:
            bot.load_extension(".".join((cogs_directory, str(cog), str(cog))))
            print(" Success!")
            cogs_loaded += 1
        except ModuleNotFoundError:
            print(" Failure!")

    print("Loaded {0} cog{1}.".format(cogs_loaded,
                                      "s" if cogs_loaded != 1 else ""))


# Main entry point to the daemon.
bot = commands.Bot(command_prefix=settings.PREFIX)
load_cogs(bot, settings.COGS_DIRECTORY)
bot.run(utilities.load_token(settings.TOKEN_NAME))
