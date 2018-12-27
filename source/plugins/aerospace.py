"""Reset the aerospace clock whenever someone mentions aerospace.

Written by Tiger Sachse.
"""

INLINE = r"(a|A)(e|E)(r|R)(o|O)(s|S)(p|P)(a|A)(c|C)(e|E)"
RESPONSE = "✈ **Resetting aerospace clock...** ✈"

async def inline_aerospace(client, message):
    """Reset the aerospace clock."""
    await client.send_message(message.channel, RESPONSE)
