import asyncio
from typing import Callable, List

class Publisher():
    def __init__(self):
        self.subscribers :List[Callable] = []

    def issue_event(self, *args, **kwargs):
        for sub in self.subscribers:
            future = sub(*args, **kwargs)
            asyncio.ensure_future(future)

    def subscribe(self, event:Callable, *args, **kwargs):
        self.subscribers.append(event)
