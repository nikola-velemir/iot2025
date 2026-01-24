from abc import ABC, abstractmethod

from shared.logger.logger import log


class BuzzerOutput(ABC):
    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
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

    def is_simulated(self) -> bool:
        return False

class GpioBuzzer(BuzzerOutput):
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self._state = False

    def on(self):
        # todo turn on gpio buzzer
        pass

    def off(self):
        # todo turn off gpio buzzer
        pass

    def is_simulated(self) -> bool:
        return False

