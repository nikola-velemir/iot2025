import time
from abc import ABC, abstractmethod
import random

from RPi import GPIO


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
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setup(self.trigger_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def read_distance(self) -> float:
        # 2ms settle
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.002)

        # Trigger pulse
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)  # 10 µs
        GPIO.output(self.trigger_pin, False)

        # Wait for echo
        timeout = 0.02
        start = time.time()
        while GPIO.input(self.echo_pin) == 0:
            if time.time() - start > timeout:
                return 0.0
        pulse_start = time.time()

        start = time.time()
        while GPIO.input(self.echo_pin) == 1:
            if time.time() - start > timeout:
                return 0.0
        pulse_end = time.time()

        distance = (pulse_end - pulse_start) * 34300 / 2
        return distance

    def is_simulated(self) -> bool:
        return False

    def cleanup(self):
        GPIO.cleanup(self.trigger_pin)
        GPIO.cleanup(self.echo_pin)
