from abc import ABC, abstractmethod


class LightInput(ABC):
    @abstractmethod
    def is_light(self)->bool:
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass
class SimulatedLightInput(LightInput):
    def __init__(self):
        self._light = False

    def turn_on(self):
        self._light = True

    def turn_off(self):
        self._light = False

    def is_light(self) -> bool:
        return self._light