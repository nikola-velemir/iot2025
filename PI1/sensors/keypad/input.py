import queue
from abc import ABC, abstractmethod
from typing import Optional

class KeypadInput(ABC):
    @abstractmethod

    def press_key(self, key: str):
        pass
    @abstractmethod
    def read_key(self) -> Optional[str]:
        pass

class SimulatedKeypad(KeypadInput):
    def __init__(self):
        self._queue = queue.Queue()

    def press_key(self, key: str):
        self._queue.put(key)

    def read_key(self):
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None