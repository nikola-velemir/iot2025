import queue
import time
from abc import ABC, abstractmethod
from typing import Optional

from RPi import GPIO


class KeypadInput(ABC):
    @abstractmethod
    def read_key(self) -> Optional[str]:
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass


class SimulatedKeypad(KeypadInput):
    def __init__(self):
        self._queue = queue.Queue()

    def press_key(self, key: str):
        self._queue.put(key)

    def read_key(self) -> Optional[str]:
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None

    def is_simulated(self) -> bool:
        return True


class GpioKeypad(KeypadInput):
    def __init__(self, pins, debounce_time=1.0):
        self._queue = queue.Queue()

        self._R1 = pins["R1"]
        self._R2 = pins["R2"]
        self._R3 = pins["R3"]
        self._R4 = pins["R4"]
        self._C1 = pins["C1"]
        self._C2 = pins["C2"]
        self._C3 = pins["C3"]
        self._C4 = pins["C4"]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._R1, GPIO.OUT)
        GPIO.setup(self._R2, GPIO.OUT)
        GPIO.setup(self._R3, GPIO.OUT)
        GPIO.setup(self._R4, GPIO.OUT)

        GPIO.setup(self._C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.setup(self._C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self._C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self._C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.debounce_time = debounce_time
        self._last_pressed_time = 0
        self._last_key = None

    def _read_line(self, line, characters) -> Optional[str]:
        GPIO.output(line, GPIO.HIGH)
        key = None
        if GPIO.input(self._C1) == 1:
            key = characters[0]
        elif GPIO.input(self._C2) == 1:
            key = characters[1]
        elif GPIO.input(self._C3) == 1:
            key = characters[2]
        elif GPIO.input(self._C4) == 1:
            key = characters[3]

        GPIO.output(line, GPIO.LOW)

        # Debounce logic
        if key:
            now = time.time()
            if key == self._last_key and (now - self._last_pressed_time) < self.debounce_time:
                return None  # ignore repeated press
            self._last_key = key
            self._last_pressed_time = now
        else:
            self._last_key = None

        return key

    def read_key(self) -> Optional[str]:
        r1_read = self._read_line(self._R1, ["1", "2", "3", "A"])
        if r1_read is not None:
            return r1_read

        r2_read = self._read_line(self._R2, ["4", "5", "6", "B"])
        if r2_read is not None:
            return r2_read
        r3_read = self._read_line(self._R3, ["7", "8", "9", "C"])
        if r3_read is not None:
            return r3_read
        r4_read = self._read_line(self._R4, ["*", "0", "#", "D"])
        if r4_read is not None:
            return r4_read
        return None

    def is_simulated(self) -> bool:
        return False
