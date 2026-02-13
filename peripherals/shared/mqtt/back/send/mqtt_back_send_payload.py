from abc import ABC, abstractmethod


class MqttBackSendPayload(ABC):
    def __init__(self, topic, type):
        self.topic = topic
        self.type = type

    @abstractmethod
    def get_payload_as_dict(self):
        pass