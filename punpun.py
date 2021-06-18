#!/usr/bin/python3
import discord
import modules.sheets as sheets
import json
from core.engine import *

class PunPun(discord.Client):
	def __init__(self, varstore=None):
		super().__init__()

		if varstore == None:
			sys.exit("Error: vars.json not loaded. Please create a vars.json file and put it in this directory.")

		self.varStore = varstore
		self.eEngine = EventEngine()

	def updatevar(self, variable: str, value):
		self.varStore.updatevar(variable, value)
		self.varStore.saveVars()

	async def on_ready(self):
		self.eEngine.issue_event("ready", message=f"Logged in as {self.user}")
	
	async def on_message(self, message):
		#don't respond to self
		if message.author == self.user:
			return
		if not message.content.startswith(self.varStore['prefix']):
			return
		else:
			cmd = message.content.split(' ', 1)[0]
			cmd = cmd[1:]
		args = message.content.split(' ', 1)
		if len(args) > 1:
			args = args[1]
		else:
			args = ''

		self.eEngine.issue_event("command", cmd.split(' ', 1)[0], args=args, msg=message)

	async def on_member_join(self, member):
		await discord.Client.get_channel(self, id=self.varStore['welcomeChannel']).send("Welcome, {}, to the AMC discord server. Enjoy your stay and introduce yourself to the others! Also please do read the rules in the {} channel.".format(member.mention, discord.Client.get_channel(self, id=self.varStore['rulesChannel']).mention))
