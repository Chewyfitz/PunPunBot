import discord
import core
from punpun import PunPun
from modules import *

###############################################################################
###############################################################################
####                                                                       ####
####             Before you run this make sure you've created              ####
####                     an appropriate vars.json file!                    ####
####                                                                       ####
###############################################################################
###############################################################################

engine = core.engine.EventEngine()

# Load the variable storage system from file 'vars.json'
vs = varStore.Store("vars.json")

# Create the client object and pass in the variable store
client = PunPun(varstore=vs)

# Start the client on the Discord API
client.run(vs['botkey'])
