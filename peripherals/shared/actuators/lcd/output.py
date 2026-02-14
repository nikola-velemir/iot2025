from abc import ABC, abstractmethod
from shared.logger.logger import log

class LcdOutput(ABC):
    @abstractmethod
    def display_text(self, line1: str, line2: str):
        pass

    @abstractmethod
    def clear(self):
        pass
    @abstractmethod
    def is_simulated(self):
        pass

class SimulatedLcd(LcdOutput):
    def is_simulated(self):
        return True

    def display_text(self, line1: str, line2: str):
        print("\n" + "="*20)
        print(f"| {line1.ljust(16)} |")
        print(f"| {line2.ljust(16)} |")
        print("="*20)

    def clear(self):
        log("LCD Screen Cleared")

class GpioLcd(LcdOutput):
    def is_simulated(self):
        return False

    def __init__(self, pin_rs, pin_e, pins_db):
         log("Hardware LCD Initialized")

    def display_text(self, line1: str, line2: str):
          pass

    def clear(self):
        pass