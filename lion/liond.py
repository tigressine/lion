import settings
from pathlib import Path
from discord.ext import commands

bot = commands.Bot(command_prefix=settings.PREFIX)


def load_token(token_name):
    """Load the Discord API authentication token."""
    with open(token_name, "r") as token_file:
        return token_file.read().strip()


def load_cogs(bot, cogs_directory):
    """"""
    cogs_path = Path(cogs_directory)
    for cog in (path.stem for path in cogs_path.iterdir()):
        try:
            bot.load_extension(".".join((cogs_directory, str(cog), str(cog))))
        except Exception as e:
            print(e)


load_cogs(bot, settings.COGS_DIRECTORY)
bot.run(load_token(settings.TOKEN_NAME))
