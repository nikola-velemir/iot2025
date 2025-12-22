from abc import ABC, abstractmethod


class ButtonInput(ABC):
    @abstractmethod
    def is_pressed(self) -> bool:
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