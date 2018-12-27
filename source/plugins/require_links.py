"""

Written by Tiger Sachse.
"""

FILTERED_CHANNELS = frozenset(("bot_testing", "personal_projects", "helpful_baubles"))

async def filter_require_links(client, message):
    """Ensure that any messages in a filtered channel contain links."""

    print(message.embeds)
    await client.send_message(message.channel, "filtered chan")
