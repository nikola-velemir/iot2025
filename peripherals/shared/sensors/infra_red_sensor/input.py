import datetime
import random
import time
from abc import abstractmethod, ABC
from collections import deque

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
        self._last_time = 0
        self._durations = deque()
        self._last_code = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ir_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(self._ir_pin)  # prevent "already registered" error

        GPIO.add_event_detect(
            self._ir_pin,
            GPIO.BOTH,
            callback=self._edge_callback
        )

    def is_simulated(self) -> bool:
        return False

    def read_key(self) -> str | None:
        if self._last_code:
            code = self._last_code
            self._last_code = None
            return code
        return None

    def _edge_callback(self, channel):
        now = time.perf_counter()
        duration = (now - self._last_time) * 1_000_000
        self._last_time = now

        if duration > 15000:
            self._durations.clear()
            return

        self._durations.append(duration)

        if len(self._durations) >= 68:
            self._decode()

    def _decode(self):
        pulses = list(self._durations)[4:]  # skip leader (4 edges)
        bits = ""

        for i in range(0, 64, 2):
            if i + 1 >= len(pulses):
                break
            space = pulses[i + 1]
            if 400 < space < 800:
                bits += "0"
            elif 1400 < space < 1800:
                bits += "1"

        self._durations.clear()

        if len(bits) != 32:
            return

        numeric = int(bits, 2)

        mapping = {
            0xff30cf: "4",
            0xff18e7: "5",
            0xff7a85: "6",
            0xff10ef: "7",
            0xff38c7: "8",
            0xff5aa5: "9",
            0xff42bd: "*",
            0xff4ab5: "0",
            0xff52ad: "#",
        }

        if numeric in mapping:
            self._last_code = mapping[numeric]