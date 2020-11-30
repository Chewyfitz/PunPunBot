# depends on varStore
from .varStore import Store
# depends on sheets
from .sheets import GoogleSheet
from datetime import datetime, timezone, date, timedelta

sheets = None

store = None

def __initStore():
	global store
	if not store:
		store = Store()

def __initSheets():
	global sheets
	if not sheets:
		sheets = GoogleSheet(GSID=store['googleSheetID']) #add Year and Month to this
		sheets.startService()

async def goodnight(args: str, msg):
	__initStore()
	__initSheets()
	userName = "{}#{}".format(msg.author.name, msg.author.discriminator)
	user = msg.author.id
	time = msg.created_at.time()

	now = datetime.now()
    print("now: {}".format(now))
    if now.time() < now.replace(hour=store['cutoffHour'], minute=0, second=0, microsecond=0).time():
        now = now - timedelta(days=1)
    day = now.day
    month = now.month
    year = now.year
	
	dt = datetime.combine(date.today(), time).replace(tzinfo=timezone.utc).astimezone(tz=None)
	time = dt.time()

	# print("user: {}".format(user))
	# print("time: {}".format(time))
	# print("now.year: {}".format(now.year))
	# print("now.month: {}".format(now.month))
	# print("day: {}".format(day))

	await sheets.sleepTime(msg.author, userName, time, year, month, day)
	await msg.add_reaction(store['emoji'])

async def setemoji(args: str, msg):
	__initStore()
	emoji = args.split(' ', 1)[0]
	store.updateVar('emoji', str(emoji))
	store.saveVars()
	await msg.channel.send("Set emoji to {}".format(str(emoji)))

async def setcutoff(args: str, msg):
	__initStore()
	cutoff = args.split(' ', 1)[0]
	store.updateVar('cutoff', cutoff)
	store.saveVars()
	await msg.channel.send("Set cutoff hour to {}".format(store['cutoffHour']))

async def ping(args: str, msg):
	await msg.channel.send("pong")
