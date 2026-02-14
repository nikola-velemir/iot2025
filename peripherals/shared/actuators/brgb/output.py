from abc import ABC, abstractmethod
from shared.logger.logger import log
from shared.mqtt.back.receive.mqtt_back_receiver import MqttReceiver
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.pubsub.subscriber import Subscriber


# Output abstraction
class BRGBOutput(ABC):
    @abstractmethod
    def is_simulated(self) -> bool:
        pass

    @abstractmethod
    def set_color(self, color: str):
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class SimulatedBRGBOutput(BRGBOutput):
    def __init__(self, name: str):
        self.name = name
        self.current_color = "OFF"

    def is_simulated(self) -> bool:
        return True

    def set_color(self, color: str):
        self.current_color = color
        log(f"[{self.name}] changed color to {color}")

    def turn_on(self):
        self.current_color = "WHITE"
        log(f"[{self.name}] turned ON")

    def turn_off(self):
        self.current_color = "OFF"
        log(f"[{self.name}] turned OFF")


class GpioBRGBOutput(BRGBOutput):
    def __init__(self, name: str, red_pin: int, green_pin: int, blue_pin: int):
        self.name = name
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.current_color = "OFF"


    def is_simulated(self) -> bool:
        return False

    def set_color(self, color: str):
        self.current_color = color
        log(f"[GPIO] {self.name} changed color to {color}")

    def turn_on(self):
        self.current_color = "WHITE"
        log(f"[GPIO] {self.name} turned ON")

    def turn_off(self):
        self.current_color = "OFF"
        log(f"[GPIO] 🌑 {self.name} turned OFF")
