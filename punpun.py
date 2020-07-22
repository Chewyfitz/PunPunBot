import discord
import sheets
import json
from datetime import datetime, timezone, date

class PunPun(discord.Client):
    def __init__(self, varstore=None):
        super().__init__()

        if varstore == None:
            sys.exit("Error: vars.json not loaded. Please create a vars.json file and put it in this directory.")

        self.varStore = varstore

        self.emoji = varstore['emoji']
        self.prefix = varstore['prefix']
        self.cutoffHour = varstore['cutoffHour']

        self.sheets = sheets.GoogleSheet(GSID=varstore['googleSheetID']) #add Year and Month to this
        self.sheets.startService()

    def updatevar(self, variable: str, value):
        self.varStore.updatevar(variable, value)
        self.varStore.saveVars()

    async def on_ready(self):
        print("Logged in as", self.user)

    def sleepTime(self, user: str, time):
        now = datetime.now()
        print("now: {}".format(now))
        if now.time() < now.replace(hour=self.varStore['cutoffHour'], minute=0, second=0, microsecond=0).time():
            day = now.day-1
        else:
            day = now.day
        
        dt = datetime.combine(date.today(), time).replace(tzinfo=timezone.utc).astimezone(tz=None)
        time = dt.time()

        # print("user: {}".format(user))
        # print("time: {}".format(time))
        # print("now.year: {}".format(now.year))
        # print("now.month: {}".format(now.month))
        # print("day: {}".format(day))

        self.sheets.sleepTime(user, time, now.year, now.month, day)
    
    async def on_message(self, message):
        #don't respond to self
        if message.author == self.user:
            return
        if not message.content.startswith(self.prefix):
            return
        else:
            cmd = message.content.split(' ', 1)[0]
            cmd = cmd[1:]
        
        if cmd.startswith("setemoji"):
            emoji = message.content.split(' ', 1)[1]
            self.updatevar('emoji', emoji)
            await message.channel.send("Set emoji to {}".format(str(emoji)))
        if cmd.startswith("setcutoff"):
            cutoff = message.content.split(' ', 1)[1]
            self.updatevar('cutoff', cutoff)
            await message.channel.send("Set cutoff hour to {}".format(self.varStore['cutoffHour']))
        if cmd == "goodnight":
            self.sleepTime("{}#{}".format(message.author.name, message.author.discriminator), message.created_at.time())
            await message.add_reaction(self.varStore['emoji'])
        # if cmd == "ping":
        #     await message.channel.send("pong")