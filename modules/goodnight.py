# depends on varStore
from .varStore import Store
# depends on sheets
from .sheets import GoogleSheet

sheets = None

store = None

def __initStore():
	if not store:
		store = Store()

def __initSheets():
	if not sheets:
		sheets = GoogleSheet(GSID=store['googleSheetID']) #add Year and Month to this
		sheets.startService()

async def goodnight(args: str, msg):
	__initStore()
	__initSheets()
	user = "{}#{}".format(msg.author.name, msg.author.discriminator)
	time = msg.created_at.time()

	now = datetime.now()
	print("now: {}".format(now))
	if now.time() < now.replace(hour=store['cutoffHour'], minute=0, second=0, microsecond=0).time():
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

	sheets.sleepTime(user, time, now.year, now.month, day)
	await msg.add_reaction(store['emoji'])

async def setemoji(args: str, msg):
	# emoji = msg.content.split(' ', 1)[1]
	store.updateVar('emoji', args)
	await msg.channel.send("Set emoji to {}".format(str(emoji)))

async def setcutoff(args: str, msg):
	# cutoff = msg.content.split(' ', 1)[1]
	store.updateVar('cutoff', args)
	await msg.channel.send("Set cutoff hour to {}".format(store['cutoffHour']))

async def ping(args: str, msg):
	await msg.channel.send("pong")