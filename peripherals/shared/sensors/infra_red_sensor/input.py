import random
from abc import abstractmethod, ABC
import time
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
        self._ir_pin = int(gpio_pin)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ir_pin, GPIO.IN)
        self._last_code = None

    def is_simulated(self) -> bool:
        return False

    def read_key(self) -> str | None:
        # 1. Wait for a signal (Pin goes LOW)
        # We don't want to block forever, so we check and return if nothing is there
        if GPIO.input(self._ir_pin) == GPIO.HIGH:
            return None

        # 2. If we are here, a signal started! Capture pulses.
        command_pulses = []
        start_time = time.perf_counter()
        last_state = GPIO.LOW

        # Timeout after 0.2s to prevent infinite loops if signal is messy
        timeout_start = time.perf_counter()

        while (time.perf_counter() - timeout_start) < 0.2:
            current_state = GPIO.input(self._ir_pin)
            if current_state != last_state:
                now = time.perf_counter()
                pulse_duration = (now - start_time) * 1_000_000
                command_pulses.append((last_state, pulse_duration))
                start_time = now
                last_state = current_state

            # If the pin stays HIGH for a long time, the transmission is over
            if current_state == GPIO.HIGH and (time.perf_counter() - start_time) > 0.05:
                break

        return self._decode_raw(command_pulses)

    def _decode_raw(self, pulses) -> str | None:
        # 1. The working script starts with '1'
        binary_str = "1"

        # 2. The working script ONLY looks at the 'rest' periods (state == 1 / HIGH)
        for state, duration in pulses:
            if state == GPIO.HIGH:
                if duration > 1000:
                    binary_str += "1"
                else:
                    binary_str += "0"

        # 3. The working script truncates specifically at 34 characters
        if len(binary_str) > 34:
            binary_str = binary_str[:34]

        # DEBUG: Uncomment this to see the hex your remote is actually sending
        # print(f"Captured Hex: {hex(int(binary_str, 2))}")

        try:
            # 4. Convert to integer using base 2
            numeric_val = int(binary_str, 2)

            # 5. Use the specific HEX values from your Buttons list
            # Note: numeric_val is an int, Buttons is a list of ints.
            for i in range(len(Buttons)):
                if Buttons[i] == numeric_val:
                    return ButtonsNames[i]

        except Exception as e:
            print(f"Logic Error: {e}")

        return None