import discord
import modules.sheets as sheets
import json

class PunPun(discord.Client):
	def __init__(self, varstore=None, cmdtree={}):
		super().__init__()

		if varstore == None:
			sys.exit("Error: vars.json not loaded. Please create a vars.json file and put it in this directory.")

		self.varStore = varstore
		self.cmdTree = cmdtree

	def updatevar(self, variable: str, value):
		self.varStore.updatevar(variable, value)
		self.varStore.saveVars()

	async def on_ready(self):
		print("Logged in as", self.user)
	
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
		
		try:
			await self.cmdTree[cmd.split(' ', 1)[0]](args=args, msg=message)
		except KeyError:
			print("KeyError: {}".format(str(cmd.split(' ', 1)[0])))


	async def on_member_join(self, member):
		await discord.Client.get_channel(self, id=self.varStore['welcomeChannel']).send("Welcome, {}, to the AMC discord server. Enjoy your stay and introduce yourself to the others! Also please do read the rules in the {} channel.".format(member.mention, discord.Client.get_channel(self, id=self.varStore['rulesChannel']).mention))