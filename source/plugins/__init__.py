"""Initializer for included Lion plugins.

This script imports all installed Lion plugins and associates their command
strings with their command functions.

Written by Tiger Sachse.
"""

from plugins import (
    egg,
    dog,
    info,
    poll,
    roles,
    sponge,
    help_menu,
    aerospace,
    user_count,
    garage_status,
    require_links,
    weather,
)

FILTERED_CHANNELS = {
    require_links.FILTERED_CHANNELS : require_links.filter_require_links
}

COMMANDS = {
    egg.COMMAND : egg.command_egg,
    dog.COMMAND : dog.command_dog,
    info.COMMAND : info.command_info,
    poll.COMMAND : poll.command_poll,
    sponge.COMMAND : sponge.command_sponge,
    roles.ADD_COMMAND : roles.command_addroles,
    roles.LIST_COMMAND : roles.command_listroles,
    help_menu.COMMAND : help_menu.command_help_menu,
    roles.REMOVE_COMMAND : roles.command_removeroles,
    user_count.COMMAND : user_count.command_user_count,
    garage_status.COMMAND : garage_status.command_garage_status,
    weather.COMMAND : weather.command_weather,
}

INLINES = {
    aerospace.INLINE : aerospace.inline_aerospace,
}
