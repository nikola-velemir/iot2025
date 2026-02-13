import random
from abc import abstractmethod, ABC


class IRInput(ABC):
    @abstractmethod
    def read_key(self) -> str:
        """Vraća hex kod dugmeta, npr. '0xFF30CF'"""
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass

class SimulatedIR(IRInput):
    def __init__(self):
        self.possible_keys = ["ON", "OFF", "RED", "GREEN", "BLUE", "BRIGHT_UP", "BRIGHT_DOWN"]

    def read_key(self) -> str | None:
        if random.random() < 0.05:
            return random.choice(self.possible_keys)
        return None

    def is_simulated(self) -> bool:
        return True