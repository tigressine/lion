"""initializer for included Lion plugins.

This script imports all installed Lion plugins and associates their command
strings with their command functions.
Written by Tiger Sachse.
"""
from plugins import (usercount,
                     available,
                     poll)

commands = {
    usercount.COMMAND : usercount.command_usercount,
    available.COMMAND : available.command_available,
    poll.COMMAND : poll.command_poll,
}
