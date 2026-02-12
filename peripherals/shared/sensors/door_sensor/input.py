from abc import ABC, abstractmethod

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

    def is_pressed(self)->bool:
        # todo check if pressed using gpio pin
        pass

    def is_simulated(self) -> bool:
        return False