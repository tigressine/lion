"""Initializer for included Lion plugins.

This script imports all installed Lion plugins and associates their command
strings with their command functions.

Written by Tiger Sachse.
"""

from plugins import (
    info,
    poll,
    roles,
    corgi,
    sponge,
    eggplant,
    help_menu,
    aerospace,
    user_count,
    garage_status,
    require_links,
)

FILTERED_CHANNELS = {
    require_links.FILTERED_CHANNELS : require_links.filter_require_links
}

COMMANDS = {
    info.COMMAND : info.command_info,
    poll.COMMAND : poll.command_poll,
    corgi.COMMAND : corgi.command_corgi,
    sponge.COMMAND : sponge.command_sponge,
    roles.ADD_COMMAND : roles.command_addroles,
    eggplant.COMMAND : eggplant.command_eggplant,
    roles.LIST_COMMAND : roles.command_listroles,
    help_menu.COMMAND : help_menu.command_help_menu,
    roles.REMOVE_COMMAND : roles.command_removeroles,
    user_count.COMMAND : user_count.command_user_count,
    garage_status.COMMAND : garage_status.command_garage_status,
}

INLINES = {
    aerospace.INLINE : aerospace.inline_aerospace,
}
