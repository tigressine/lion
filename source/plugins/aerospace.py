"""Reset the aerospace clock whenever someone mentions aerospace.

Written by Tiger Sachse.
"""
import random

INLINE = r"(a|A)(e|E)(r|R)(o|O)(s|S)(p|P)(a|A)(c|C)(e|E)"
RESPONSE = "✈ **Did I hear aerospace?** ✈"
ODDS = .1

async def inline_aerospace(client, message):
    """Reset the aerospace clock."""
    if random.random() < ODDS:
        await message.channel.send(RESPONSE)
