from abc import ABC, abstractmethod
import random

from RPi import GPIO


class MotionInput(ABC):
    @abstractmethod
    def is_motion(self) -> bool:
        """Return True if motion is detected"""
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass

class SimulatedMotionInput(MotionInput):
    def __init__(self):
        self._motion = False

    def is_motion(self) -> bool:
        return random.choice([True, False])

    def is_simulated(self) -> bool:
        return True

class GpioMotionInput(MotionInput):
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self._motion = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN)

    def is_motion(self) -> bool:
        return GPIO.input(self.gpio_pin) == GPIO.HIGH


    def is_simulated(self) -> bool:
        return False
