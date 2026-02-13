from abc import ABC

from shared.pubsub.subscriber import Subscriber


class Publisher(ABC):
    def __init__(self):
        self._subscribers = []
    def subscribe(self, sub:Subscriber):
        self._subscribers.append(sub.callback)
    def subscribe_multiple(self, subs:list[Subscriber]):
        for sub in subs:
            self._subscribers.append(sub.callback)

    def notify(self, event):
        for sub in self._subscribers:
            sub(event)