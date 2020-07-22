import discord
from punpun import PunPun
from varStore import Store

# Load the var store from file 'vars.json' (can set any path if you want)
varStore = Store("vars.json")
varStore.loadVars()

# Create the client object and pass in the variable store
client = PunPun(varstore=varStore)
key = varStore['botkey']

# Start the client on the Discord API
client.run(key)