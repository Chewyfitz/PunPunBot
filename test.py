from modules import *

print([globals()[x] for x in dir() if not x.startswith('_')])
