# depends on varStore
import varStore
# depends on sheets
import sheets

store = Store()
sheets = sheets.GoogleSheet(GSID=store['googleSheetID']) #add Year and Month to this
sheets.startService()

def goodnight(msg):
	print("Goodnight")

def setemoji(msg):
	print("Set Emoji")

def setcutoff(msg):
	print("Set cutoff")
