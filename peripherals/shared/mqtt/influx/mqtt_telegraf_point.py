import time


class MqttTelegrafPoint:
    def __init__(self, type_name, device_name, name, value, is_simulated):
        self.type_name = type_name
        self.device_name = device_name
        self.name = name
        self.value = value
        self.is_simulated = is_simulated
        self.time = time.time_ns()