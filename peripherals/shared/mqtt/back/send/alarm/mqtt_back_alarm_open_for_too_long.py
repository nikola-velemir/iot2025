from shared.mqtt.back.send.mqtt_back_send_payload import MqttBackSendPayload


class MqttBackAlarmOpenForTooLongPayload(MqttBackSendPayload):
    def get_payload_as_dict(self):
        return { "type": self.type }

    def __init__(self):
        super().__init__("back_send/alarm", "open_too_long")
