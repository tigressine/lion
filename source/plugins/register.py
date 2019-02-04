"""Register and unregister from classes to show/hide
them in the sidebar

Written by Sam Shannon
"""

import re
import discord

LIST_COMMAND = "listclasses"
REGISTER_COMMAND = "register"
UNREGISTER_COMMAND = "unregister"

LIST_COMMAND_FORMAT = r"^!{0}$".format(LIST_COMMAND)
REGISTER_COMMAND_FORMAT = r"^!{0}( [a-zA-Z0-9_ ]+)$".format(REGISTER_COMMAND)
UNREGISTER_COMMAND_FORMAT = r"^!{0}( [a-zA-Z0-9_ ]+)$".format(UNREGISTER_COMMAND)

CLASS_PATTERN = re.compile(r"(?P<short>[a-z0-9]+)_(?P<prof>[a-z]+)$")

ALLOWED_CATEGORIES = ["CLASSES"]


class Class:
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel

    def contains_member(self, member):
        return self.channel.permissions_for(member).read_messages


async def command_list(client, message):
    """List the available classes"""

    response = "**All classes:**\n```\n"

    # show class details
    classes = await get_classes(message.guild)
    for class_ in classes:
        arrow = "-->" if class_.contains_member(message.author) else ""
        response += "{:4}{}\n".format(arrow, class_.name)

    response += "```\nYour classes are highlighted with an arrow.\n" \
        "You can manage your classes with `!{}` and `!{}`".format(REGISTER_COMMAND, UNREGISTER_COMMAND)
    await message.channel.send(response)


async def command_register(client, message):
    """Give member access to requested class channels"""

    # check command syntax
    command_match = re.match(REGISTER_COMMAND_FORMAT, message.content)
    if command_match is None:
        response = "Incorrect command syntax. Try `!help`."
        await message.channel.send(response)
        return

    # get the requested classes
    cfm = await get_classes_from_message(message)
    if cfm is None:
        return
    classes = cfm[0]
    isAll = cfm[1]

    # give permissions
    for class_ in classes:
        await class_.channel.set_permissions(message.author, read_messages=True)

    # output the registered classes
    if not isAll:
        response = "Registered classes:"
        for class_ in classes:
            response += "\n<#{}>".format(class_.channel.id)
    else:
        response = "Registered all classes."
    await message.channel.send(response)


async def command_unregister(client, message):
    """Remove access to requested class channels"""

    # check command syntax
    command_match = re.match(UNREGISTER_COMMAND_FORMAT, message.content)
    if command_match is None:
        response = "Incorrect command syntax. Try `!help`."
        await message.channel.send(response)
        return

    # get the requested classes
    cfm = await get_classes_from_message(message)
    if cfm is None:
        return
    classes = cfm[0]

    # remove permissions
    for class_ in classes:
        await class_.channel.set_permissions(message.author, read_messages=False)

    # reply
    response = "Unregistered from classes."
    await message.channel.send(response)


async def get_classes_from_message(message):
    """Get classes user referenced in their message"""
    possible_classes = await get_classes(message.guild)
    req_class_names = message.content.split()[1:]

    # if only "all", return all classes
    if len(req_class_names) == 1 and req_class_names[0].lower() == "all":
        return (possible_classes, True)

    # find the requested classes
    req_class_names = set(req_class_names)
    classes = []
    for req_class_name in req_class_names:
        req_class_name = req_class_name.lower()

        # class group
        if "_" not in req_class_name:
            for possible_class in possible_classes:
                if possible_class.name.split('_')[0].strip() == req_class_name.strip():
                    classes.append(possible_class)
            if len(classes) == 0:
                response = "`{}` is not an available class group. Try `!{}`." \
                    .format(req_class_name, LIST_COMMAND)
                await message.channel.send(response)
                return

        # individual class
        else:
            for possible_class in possible_classes:
                if req_class_name == possible_class.name:
                    classes.append(possible_class)
                    break
            else:
                response = "`{}` is not an available class. Try `!{}`." \
                    .format(req_class_name, LIST_COMMAND)
                await message.channel.send(response)
                return
    
    return (classes, False)


async def get_classes(guild):
    # get all classes in the ALLOWED_CATEGORIES
    classes = []
    for category in guild.categories:
        if category.name.upper() in ALLOWED_CATEGORIES:
            for channel in category.channels:
                class_ = Class(channel.name, channel)
                classes.append(class_)

    return classes
