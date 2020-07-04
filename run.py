import discord
import json
import os.path
from punpun import PunPun
from datetime import datetime



if(os.path.exists("vars.json")):
    f = open("vars.json", "r")
    v = f.read()
    print(v)
    vs = json.loads(v)
    client = PunPun(emoji=vs['emoji'], prefix=vs['prefix'], cutoffHour=vs['cutoffHour'], googleSheetID=vs['googleSheetID'])
    key = vs['botkey']
else:
    client = PunPun()

client.run(key)