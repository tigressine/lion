"""Initializer for included Lion plugins.

This script imports all installed Lion plugins and associates their command
strings with their command functions.

Written by Tiger Sachse.
"""

from plugins import (
    user_count,
    help_menu,
    poll,
    aerospace,
    garage_status,
    roles,
    corgi,
    gulag,
    sponge,
    request,
)

COMMANDS = {
    user_count.COMMAND : user_count.command_user_count,
    help_menu.COMMAND : help_menu.command_help_menu,
    poll.COMMAND : poll.command_poll,
    garage_status.COMMAND : garage_status.command_garage_status,
    sponge.COMMAND : sponge.command_sponge,
    roles.COMMAND : roles.command_roles,
    corgi.COMMAND : corgi.command_corgi,
    gulag.COMMAND : gulag.command_gulag,
    request.REQUEST_COMMAND : request.command_request,
    request.REQUESTS_COMMAND : request.command_requests_management,
    request.RESPOND_COMMAND : request.command_respond,
}

INLINES = {
    aerospace.INLINE : aerospace.inline_aerospace,
}
