from shared.mqtt.back.send.mqtt_back_send_payload import MqttBackSendPayload


class MqttBackAlarmMotionPayload(MqttBackSendPayload):
    def get_payload_as_dict(self):
        return { "motion": self.motion, "type": self.type }

    def __init__(self, motion):
        super().__init__("back_send/alarm", "motion")
        self.motion = motion