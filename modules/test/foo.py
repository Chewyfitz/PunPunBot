from modules.core import export

@export
def foo(x):
	print("Hello, " + x)

def bar(x):
	print("How did you get here, " + x + "?")