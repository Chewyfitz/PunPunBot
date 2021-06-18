import discord
from typing import Callable
from .publisher import Publisher

class EventEngine():
    # Using a singleton pattern in Python allows us to create an EventEngine 
    #   from anywhere and be able to call the list of events
    class __singleton_Engine():
        def __init__(self):
            # Do some stuff to init
            self.publishers = {}
            print("Init done.")

        # Create an event type publisher queue
        def register_pub(self, publisher:Publisher, name:str):
            if name not in self.publishers:
                # Create a publisher queue for this event name if one doesn't exist
                self.publishers[name] = []
            # Append this publisher to the end of the event queue
            self.publishers[name].append(publisher)

        # Register an event to a publisher queue
        def subscribe_to(self, event:Callable, name:str, *args, **kwargs) -> bool:
            if name not in self.publishers:
                # There were no publishers for this event type
                print(f"{name} not found in publishers - {self.publishers}")
                return False

            for publisher in self.publishers[name]:
                publisher.subscribe(event, *args, **kwargs)
            # At least one publisher exists, but it didn't necessarily get called
            return True

        # Issue an event to the list of publishers listening for event name
        def issue_event(self, name:str, *args, **kwargs):
            if name not in self.publishers:
                # We don't have any publishers for that event type
                return

            for publisher in self.publishers[name]:
                publisher.issue_event(*args, **kwargs)

    __engine = None

    def __init__(self):
        self.__engine = self.__class__.__engine
        if self.__engine == None:
            self.__class__.__engine = self.__class__.__singleton_Engine()
            self.__engine = self.__class__.__engine

    def register_pub(self, publisher:Publisher, name:str):
        self.__engine.register_pub(publisher, name)

    def subscribe_to(self, event:Callable, name:str, *args, **kwargs) -> bool:
        return self.__engine.subscribe_to(event, name, *args, **kwargs)

    def issue_event(self, name:str, *args, **kwargs):
        self.__engine.issue_event(name, *args, **kwargs)

