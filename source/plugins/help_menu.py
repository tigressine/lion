"""Still garbage, will revisit."""
COMMAND = "help"

import discord

async def command_help_menu(client, message):
    """"""
    response = "Hey there! Here's a list of commands that I understand:"

    embedded_message = discord.Embed(color=0x81f97c)
    embedded_message.add_field(
        name="!users",
        value="Display the latest server membership count.",
        inline=False
    )

    embedded_message.add_field(
        name="!poll time{s|m|h|d} \`prompt\` \`choice1;choice2;etc\`",        
        value="Create a new poll.",
        inline=False
    )

    embedded_message.add_field(
        name="!garage [garage]",
        value="See the status of UCF parking garages.",
        inline=False
    )

    embedded_message.add_field(
        name="!sponge message",
        value="Say hi to Spongebob.",
        inline=False
    )
    
    embedded_message.add_field(
        name="!roles [sub-command]",
        value="Manage your roles. Run `!roles help` for more info",
        inline=False
    )
    
    embedded_message.add_field(
      name="!corgi",
      value="Posts a corgi picture FOR FREE :)",
      inline=False
    )
    embedded_message.add_field(
      name="!gulag [userToGulag] [reason for gulag]",
      value="Posts a corgi picture FOR FREE :)",
      inline=False
    )

    await client.send_message(message.channel, response, embed=embedded_message)
