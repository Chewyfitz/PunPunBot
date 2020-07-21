import discord
from punpun import PunPun
from datetime import datetime
from varStore import Store

varStore = Store("vars.json")
varStore.loadVars()


client = PunPun(emoji=varStore['emoji'], prefix=varStore['prefix'], cutoffHour=varStore['cutoffHour'], googleSheetID=varStore['googleSheetID'])
key = varStore['botkey']


client.run(key)