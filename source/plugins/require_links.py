"""Require that all posts in filtered channels contain valid hyperlinks.

This is useful for reducing/eliminating conversation in channels that link to
personal projects or helpful information.

Written by Tiger Sachse.
"""

import re
import httplib2

URL_FORMAT = "(?P<url>https?://\S+)"
FILTERED_CHANNELS = frozenset(("personal_projects", "helpful_baubles"))
NO_LINK_WARNING_FORMAT = (
    "The channel #{0} is a repository for links, not a place for discussion. "
    + "Any post in this channel must include a valid link, but yours did not."
    + "\n\nYour original post:\n```{1}```"
)
INVALID_LINK_WARNING_FORMAT = (
    "All posts in #{0} must contain active links. Your post's link was invalid."
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
            NO_LINK_WARNING_FORMAT.format(message.channel, message.content)
        )

    # Otherwise, check the validity of the link. If it is invalid, delete
    # the new message and DM the author.
    elif is_invalid(search.group("url")):
        await client.delete_message(message)
        await client.send_message(
            message.author,
            INVALID_LINK_WARNING_FORMAT.format(
                message.channel,
                message.content
            )
        )

def is_invalid(link):
    """Check if a link is invalid by requesting its header."""
    try:
        response = httplib2.Http().request(link, "HEAD")
    except httplib2.HttpLib2Error:
        return True
    
    return False if int(response[0]["status"]) < 400 else True
