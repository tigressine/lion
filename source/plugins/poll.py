poll_emojis = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]

async def command_poll(client, message):
    response = "poll 1 or 2 which is better?"
    poll = await client.send_message(message.channel, response)
    print(poll.content)
    for emoji in poll_emojis:
        await client.add_reaction(poll, emoji)
