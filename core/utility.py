import modules
import datetime
import discord
from .listen import subscribe

from .engine import EventEngine

@subscribe("ready")
async def ready_print(message:str=""):
    print(message)

@subscribe("command", cmd="list_functions")
async def list_functions(args:str, msg):
    mods = [modules.__dict__[m] for m in vars(modules) if not m.startswith('_')]

    loaded_modules = ""
    for module in mods:
        if loaded_modules != "":
            loaded_modules += ", "
        loaded_modules += module.__name__

    funcs = EventEngine()._EventEngine__engine.publishers["command"][0].commandTree.keys()

    functions = ""
    for f in funcs:
        if functions != "":
            functions += ", "
        functions += f
    
    embed = discord.Embed(
        title="Loaded Modules", 
        description=loaded_modules, 
        colour=discord.Colour(0xa3de23), 
        timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
    embed.add_field(name="Loaded Functions:", value=functions)
    await msg.channel.send(embed=embed)

@subscribe("command", cmd="unroll", aliases=[])
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
