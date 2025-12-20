from abc import ABC, abstractmethod
import random

class UltrasonicInput(ABC):
    @abstractmethod
    def read_distance(self) -> float:
        """Return distance"""
        pass



class SimulatedUltrasonicInput(UltrasonicInput):
    def __init__(self):
        self._distance = 1.0

    def read_distance(self) -> float:
        self._distance += random.uniform(-0.1, 0.1)
        self._distance = max(0.2, min(4.0, self._distance))
        return self._distance