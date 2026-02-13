from shared.mqtt.back.send.mqtt_back_send_payload import MqttBackSendPayload


class MqttBackAlarmDoorPersonEventPayload(MqttBackSendPayload):
    def get_payload_as_dict(self):
        return { "person_event": self.person_event, "type": self.type }

    def __init__(self, person_event):
        super().__init__("back_send/alarm", "person_event")
        self.person_event = person_event