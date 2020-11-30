import discord
from punpun import PunPun
from modules import *

del modules # kill recursion.

# from modules.varStore import Store
# from modules.goodnight import goodnight, setemoji, setcutoff

###############################################################################
###############################################################################
####                                                                       ####
####             Before you run this make sure you've created              ####
####                     an appropriate vars.json file!                    ####
####                                                                       ####
###############################################################################
###############################################################################

# Load the var store from file 'vars.json' (can set any path if you want)
# - varStore should be initialised first if you want to decide the location of `vars.json`.
# - If you don't call varStore.loadVars() then the vars won't be loaded ;)
vs = varStore.Store("vars.json")
vs.loadVars()

# Generate the command parsing tree
# TEMPORARILY DEFINED AS A STATIC TREE DURING DEVELOPMENT
# WILL BE MODIFIED TO GENERATE PROGRAMMATICALLY
cmdTree = {'goodnight': goodnight.goodnight
		  ,'setemoji': goodnight.setemoji
		  ,'setcutoff': goodnight.setcutoff
          ,'unroll': core.unroll
		  }

# Create the client object and pass in the variable store
client = PunPun(varstore=vs, cmdtree=cmdTree)
key = vs['botkey']

# Start the client on the Discord API
client.run(key)