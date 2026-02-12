from abc import ABC, abstractmethod


class DHTInput(ABC):
    @abstractmethod
    def read_data(self):
        """Returns (temperature, humidity)"""
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass


class SimulatedDHT(DHTInput):
    def __init__(self):
        self.temp = 25.0
        self.hum = 50.0

    def set_data(self, temp, hum):
        self.temp = temp
        self.hum = hum

    def read_data(self):
        return self.temp, self.hum

    def is_simulated(self) -> bool:
        return True


class GpioDHT(DHTInput):
    def __init__(self, gpio_pin):
        self.pin = gpio_pin

    def read_data(self):
        # Todo: Implementation for physical sensor
        return 22.0, 45.0

    def is_simulated(self) -> bool:
        return False