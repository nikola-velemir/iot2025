from abc import ABC, abstractmethod
import board
import adafruit_dht


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
    def __init__(self, gpio_pin: int):
        self._sensor = adafruit_dht.DHT11(getattr(board, f"D{gpio_pin}"))

    def read_data(self):
        temperature = self._sensor.temperature
        humidity = self._sensor.humidity

        if temperature is None or humidity is None:
            raise IOError("Failed to read DHT11")

        return temperature, humidity

    def is_simulated(self) -> bool:
        return False