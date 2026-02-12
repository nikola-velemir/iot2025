import time


class MqttBackSendPayload:
    def __init__(self, type_name, name, value):
        self.type_name = type_name
        self.name = name
        self.value = value
        self.time = time.time_ns()