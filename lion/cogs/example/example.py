"""An example cog for educational purposes.

This cog creates a new command called 'example' which takes 1 argument: a
number. This cog loads a text file from 'data/' based on the given number and
then posts the contents of that file to the user's server. Since this cog is
named 'example.py' it must be located inside of a directory named 'example'
within the 'cogs' directory. The directory name and Python source file name
must match.

Written by Tiger Sachse.
"""

# The utilities module provides necessary functions like respond() and
# throw_error(). Use these functions to interact with the Discord API, instead
# of the functions provided directly by the API.
import utilities
from discord.ext import commands


def setup(bot):
    """Add this cog to a given bot.

    Every cog must include this function.
    """
    bot.add_cog(ExampleCog(bot))


class ExampleCog(commands.Cog):
    """This class contains all the logic for the 'example' command."""

    # Notice that paths for data must be relative and must start at the
    # 'cogs' directory. If you try to access 'data/example{0}.txt' the program
    # will not understand because of how Python keeps track of relative paths.
    EXAMPLE_PATH_FORMAT = "cogs/example/data/example{0}.txt"
    
    @commands.command(name="example", usage="!example <number>")
    async def example_command(self, context, number: int):
        """Display some example text.
        
        The first line of this docstring is displayed in the !help command's
        menu. The 'usage' parameter passed to this function's decorator is also
        used.
        """

        # Do not handle errors directly in your cog_command() function. Raise
        # the appropriate exception and let the cog_error() function handle it.
        if number < 1 or number > 3:
            raise commands.errors.BadArgument("Number out of range.")

        # Use the respond() function to send text to the user's server. This
        # function accepts all the same arguments that context.send() accepts.
        await utilities.respond(context, self.get_example_text(number))

    @example_command.error
    async def example_error(self, context, error):
        """Handle any errors that occur during the 'example' command.
        
        This function passes the error and the context to the throw_error()
        function which outputs the error to the user's server. You can add code
        here to ignore certain errors or do other, more complicated things.
        """
        await utilities.throw_error(context, error)

    def get_example_text(self, number):
        """Load text from a file."""
        with open(self.EXAMPLE_PATH_FORMAT.format(number), "r") as example_file:
            return example_file.read()
