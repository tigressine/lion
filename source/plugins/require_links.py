"""Require that all posts in filtered channels contain hyperlinks.

This is useful for reducing/eliminating conversation in channels that link to
personal projects or helpful information.

Written by Tiger Sachse.
"""

import re

URL_FORMAT = "(?P<url>https?://\S+)"
FILTERED_CHANNELS = frozenset(("personal_projects", "helpful_baubles"))
WARNING_FORMAT = (
    "The channel #{0} is a repository for links, not a place for discussion. "
    + "Any post in this channel must include a valid link, but yours did not."
    + "\n\nYour original post:\n```{1}```"
)

async def filter_require_links(client, message):
    """Ensure that all new messages in any filtered channel contain links."""
    search = re.search(URL_FORMAT, message.content)

    # If no link was found, delete the new message and DM the author.
    if search is None:
        await client.delete_message(message) 
        await client.send_message(
            message.author,
            WARNING_FORMAT.format(message.channel, message.content)
        )
