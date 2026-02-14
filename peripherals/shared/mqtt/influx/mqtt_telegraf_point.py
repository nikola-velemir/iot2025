import time
from abc import ABC, abstractmethod


class MqttTelegrafPoint(ABC):
    def __init__(self, type_name, device_name, name, is_simulated):
        self.type_name = type_name
        self.device_name = device_name
        self.name = name
        self.is_simulated = is_simulated
        self.time = time.time_ns()

    @abstractmethod
    def get_value(self):
        pass