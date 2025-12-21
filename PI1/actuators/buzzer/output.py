from abc import ABC, abstractmethod

from logger.logger import log


class BuzzerOutput(ABC):
    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass
    
class SimulatedBuzzer(BuzzerOutput):
    def __init__(self):
        self._state = False

    def on(self):
        if not self._state:
            self._state = True
            log("Buzzer ON!")

    def off(self):
        if self._state:
            self._state = False
            log("Buzzer OFF!")
