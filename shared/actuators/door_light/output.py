from abc import ABC, abstractmethod


class LightOutput(ABC):
    @abstractmethod
    def is_light(self) -> bool:
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass

class SimulatedLightOutput(LightOutput):
    def __init__(self):
        self._light = False

    def turn_on(self):
        self._light = True

    def turn_off(self):
        self._light = False

    def is_light(self) -> bool:
        return self._light

    def is_simulated(self) -> bool:
        return True


class GpioLightOutput(LightOutput):
    def __init__(self, gpio_pin):
        self.gpio_pin = gpio_pin
        self._light = False

    def turn_on(self):
        # todo gpio turn on light
        pass

    def turn_off(self):
        # todo gpio turn off light
        pass

    def is_light(self) -> bool:
        return self._light

    def is_simulated(self) -> bool:
        return False