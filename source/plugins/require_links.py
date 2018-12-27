"""

Written by Tiger Sachse.
"""

import re

URL_FORMAT = "(?P<url>https?://\S+)"
FILTERED_CHANNELS = frozenset(("bot_testing", "personal_projects", "helpful_baubles"))
NO_LINK_WARNING_FORMAT = (
    "The channel #{0} is a repository for links, not a place for discussion. "
    + "Any post in this channel must include a valid link, but yours did not."
    + "\n\nYour original post:\n```{1}```"
)

async def filter_require_links(client, message):
    """Ensure that any messages in a filtered channel contain links."""

    search = re.search(URL_FORMAT, message.content)
    if search is None:
        await client.delete_message(message) 
        await client.send_message(
            message.author,
            NO_LINK_WARNING_FORMAT.format(message.channel, message.content)
        )
    else:
        await client.send_message(message.channel, "noice")
