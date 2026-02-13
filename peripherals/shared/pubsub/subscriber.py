from abc import ABC, abstractmethod


class Subscriber(ABC):
    @abstractmethod
    def callback(self, event):
        pass