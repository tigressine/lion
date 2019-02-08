import utilities
from discord.ext import commands

def setup(bot):
    bot.add_cog(ExampleCog())


class ExampleCog:
    EXAMPLE_PATH_FORMAT = "cogs/example/assets/example{0}.txt"
    
    @commands.command(name="example")
    async def example_command(self, context, number: int):
        """"""
        if number < 1 or number > 3:
            raise commands.errors.BadArgument("Number out of range.")
        await utilities.respond(context, self.get_example_text(number))

    @example_command.error
    async def on_example_error(self, context, error):
        """"""
        await utilities.throw_error(context, error)

    def get_example_text(self, number):
        """"""
        with open(self.EXAMPLE_PATH_FORMAT.format(number), "r") as example_file:
            return example_file.read()
