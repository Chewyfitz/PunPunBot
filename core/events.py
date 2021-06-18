from .publisher import *
from .commandPublisher import *
from .engine import *

"""
This file defines the core event types used by discord.py, and a couple of core 
events used for managing variables, etc.
Feel free to define your own events either here or in a separate file, though 
keep in mind you'll need to include your extra event definitions somehow so they
are actually executed.
"""

_e = EventEngine()

on_message = Publisher()
_e.register_pub(on_message, "message")

on_command = CommandPublisher()
_e.register_pub(on_command, "command")

on_ready = Publisher()
_e.register_pub(on_ready, "ready")

on_join = Publisher()
_e.register_pub(on_join, "join")

on_leave = Publisher()
_e.register_pub(on_leave, "leave")


