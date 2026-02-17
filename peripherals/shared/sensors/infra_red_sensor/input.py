import datetime
import random
import time
from abc import abstractmethod, ABC

from RPi import GPIO


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


Buttons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897, 0x300ff02fd,
           0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff4ab5,
           0x300ff52ad]  # HEX code list
ButtonsNames = ["LEFT", "RIGHT", "UP", "DOWN", "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0",
                "#"]  # String list in same order as HEX list

class GpioIR(IRInput):
    def __init__(self, gpio_pin):
        self._ir_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ir_pin, GPIO.IN)

    def read_key(self) -> str | None:
        binary_str = self._get_binary()
        if not binary_str:
            return None
        in_data = self._convert_hex(binary_str)

        for button, code in zip(ButtonsNames, Buttons):
            if in_data == hex(code):
                return button
        return None

    def is_simulated(self) -> bool:
        return False

    def _get_binary(self) -> str | None:
        """Reads raw IR pulses and converts them to a binary string."""
        command = []
        previous_value = GPIO.input(self._ir_pin)

        # Wait for pin to go low (start of IR pulse)
        while previous_value:
            time.sleep(0.001)
            previous_value = GPIO.input(self._ir_pin)

        start_time = datetime.now()
        num_ones = 0

        while True:
            value = GPIO.input(self._ir_pin)
            if value != previous_value:
                now = datetime.now()
                pulse_time = (now - start_time).total_seconds() * 1_000_000  # microseconds
                start_time = now
                command.append((previous_value, int(pulse_time)))

            if value:
                num_ones += 1
            else:
                num_ones = 0

            if num_ones > 10000:
                break

            previous_value = value

        # Convert pulses to binary string
        binary_str = ""
        for val, duration in command:
            if val == 1:  # Rest period
                binary_str += "1" if duration > 1000 else "0"

        if len(binary_str) > 34:
            binary_str = binary_str[:34]

        return binary_str or None

    def _convert_hex(self, binary_str: str) -> str:
        return hex(int(binary_str, 2))