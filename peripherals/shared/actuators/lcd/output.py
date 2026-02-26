from abc import ABC, abstractmethod

from RPLCD.i2c import CharLCD
from RPi import GPIO

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
        print("\n" + "=" * 20)
        print(f"| {line1.ljust(16)} |")
        print(f"| {line2.ljust(16)} |")
        print("=" * 20)

    def clear(self):
        log("LCD Screen Cleared")


class GpioLcd(LcdOutput):
    def __init__(self, address=0x27):
        log("Hardware I2C LCD Initialized")

        self.lcd = CharLCD(
            i2c_expander='PCF8574',
            address=address,
            port=1,
            cols=16,
            rows=2
        )

    def is_simulated(self):
        return False

    def display_text(self, line1: str, line2: str):
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(line1[:16].ljust(16))

        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(line2[:16].ljust(16))

    def clear(self):
        self.lcd.clear()
