import queue
from abc import ABC, abstractmethod
from typing import Optional

class KeypadInput(ABC):
    @abstractmethod
    def read_key(self) -> Optional[str]:
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass

class SimulatedKeypad(KeypadInput):
    def __init__(self):
        self._queue = queue.Queue()

    def press_key(self, key: str):
        self._queue.put(key)

    def read_key(self) -> Optional[str]:
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None

    def is_simulated(self) -> bool:
        return True

class GpioKeypad(KeypadInput):
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self._queue = queue.Queue()

    def read_key(self) -> Optional[str]:
        # todo read key from gpio pin
        pass

    def is_simulated(self) -> bool:
        return False