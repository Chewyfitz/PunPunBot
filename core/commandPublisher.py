import asyncio
from typing import Callable
from .publisher import *

class CommandPublisher(Publisher):
    def __init__(self):
        # Don't need to call super().__init__() because we're overriding the
        #   behaviour anyway.
        # super().__init__()
        self.commandTree = {}

    def issue_event(self, command, *posargs, **kwargs):
        if command not in self.commandTree:
            return
        
        for sub in self.commandTree[command]:
            future = sub(*posargs, **kwargs)
            asyncio.ensure_future(future)

    def subscribe(self, event:Callable, cmd:str="", aliases=[], *args, **kwargs):
        if cmd not in self.commandTree:
            self.commandTree[cmd] = []

        self.commandTree[cmd].append(event)

        print(f"registered command: {cmd}")

        for alias in aliases:
            self.subscribe(event, cmd=alias)
