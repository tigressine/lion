"""Initializer for included Lion plugins.

This script imports all installed Lion plugins and associates their command
strings with their command functions.

Written by Tiger Sachse.
"""

from plugins import (
    info,
    poll,
    roles,
<<<<<<< HEAD
#   corgi,                  removed until API key issue is solved
=======
    dog,
>>>>>>> 3039d0ee5a93d6d900584c2608ae9c0ea93989e4
    sponge,
    eggplant,
    help_menu,
#   aerospace,
    user_count,
#   garage_status,
    require_links,
)

FILTERED_CHANNELS = {
    require_links.FILTERED_CHANNELS : require_links.filter_require_links
}

COMMANDS = {
    info.COMMAND : info.command_info,
    poll.COMMAND : poll.command_poll,
<<<<<<< HEAD
#   corgi.COMMAND : corgi.command_corgi,
=======
    dog.COMMAND : dog.command_dog,
>>>>>>> 3039d0ee5a93d6d900584c2608ae9c0ea93989e4
    sponge.COMMAND : sponge.command_sponge,
    roles.ADD_COMMAND : roles.command_addroles,
    eggplant.COMMAND : eggplant.command_eggplant,
    roles.LIST_COMMAND : roles.command_listroles,
    help_menu.COMMAND : help_menu.command_help_menu,
    roles.REMOVE_COMMAND : roles.command_removeroles,
    user_count.COMMAND : user_count.command_user_count,
#   garage_status.COMMAND : garage_status.command_garage_status,
}

INLINES = {
#    aerospace.INLINE : aerospace.inline_aerospace,
}
