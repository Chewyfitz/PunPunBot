from .export import export
import datetime
import discord

@export
async def unroll(args, msg):
    list = []
    m=msg
    list.append(m)
    while(m.reference):
        m = (await m.channel.fetch_message(m.reference.message_id))
        list.append(m)
    list.reverse()

    embed = discord.Embed(title="Unrolled Thread", colour=discord.Colour(0xa3de23), timestamp=datetime.datetime.now(datetime.timezone.utc))

    for m in list:
        embed.add_field(name=m.author, value=m.content, inline=False)

    print(list)
    await msg.channel.send(embed=embed)