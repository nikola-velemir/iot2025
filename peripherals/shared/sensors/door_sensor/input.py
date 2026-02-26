from abc import ABC, abstractmethod

from RPi import GPIO


class ButtonInput(ABC):
    @abstractmethod
    def is_pressed(self) -> bool:
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass

class SimulatedButton(ButtonInput):
    def __init__(self):
        self._pressed = False


    def press(self):
        self._pressed = True

    def release(self):
        self._pressed = False

    def is_pressed(self)->bool:
        return self._pressed

    def is_simulated(self) -> bool:
        return True

class GpioButton(ButtonInput):
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self._pressed = False
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_pressed(self)->bool:
        return GPIO.input(self.gpio_pin) == GPIO.LOW

    def is_simulated(self) -> bool:
        return False