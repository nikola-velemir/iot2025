from shared.mqtt.back.send.mqtt_back_send_payload import MqttBackSendPayload


class MqttBackAlarmArmPayload(MqttBackSendPayload):
    def get_payload_as_dict(self):
        return { "pin": self.pin, "type": self.type }

    def __init__(self, pin):
        super().__init__("back_send/alarm", "try_arm")
        self.pin = pin