from abc import ABC, abstractmethod
import random

class UltrasonicInput(ABC):
    @abstractmethod
    def read_distance(self) -> float:
        """Return distance"""
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass

class SimulatedUltrasonicInput(UltrasonicInput):
    def __init__(self):
        self._distance = 1.0

    def read_distance(self) -> float:
        self._distance += random.uniform(-0.1, 0.1)
        self._distance = max(0.2, min(4.0, self._distance))
        return self._distance

    def is_simulated(self) -> bool:
        return True

class GpioUltrasonicInput(UltrasonicInput):
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self._distance = 1.0

    def read_distance(self) -> float:
        # todo read distance off GPIO pin
        pass

    def is_simulated(self) -> bool:
        return False