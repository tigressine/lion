"""Initializer for included Lion plugins.

This script imports all installed Lion plugins and associates their command
strings with their command functions.

Written by Tiger Sachse.
"""
from plugins import (user_count,
                     help_menu,
                     poll,
                     aerospace,
                     garage_status)

COMMANDS = {
    user_count.COMMAND : user_count.command_user_count,
    help_menu.COMMAND : help_menu.command_help_menu,
    poll.COMMAND : poll.command_poll,
    garage_status.COMMAND : garage_status.command_garage_status,
}

INLINES = {
    aerospace.INLINE : aerospace.inline_aerospace,
}
