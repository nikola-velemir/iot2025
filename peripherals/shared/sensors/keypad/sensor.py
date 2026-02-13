from shared.subscriber.subscriber import Subscriber
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.sensors.keypad.input import KeypadInput
from shared.logger.logger import log


class KeyPad:
    def __init__(self, keypad: KeypadInput, name, device_name, mqtt_client):
        self.keypad = keypad
        self._subscribers = []
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttTelegrafBatchClient = mqtt_client

    def subscribe(self, subscriber: Subscriber):
        self._subscribers.append(subscriber.callback)

    def poll(self):
        key = self.keypad.read_key()
        if key:
            self.on_key_pressed(key)

    def on_key_pressed(self, key: str):
        self.mqtt_client.send(
            MqttTelegrafPoint(
                "KeypadSensor",
                self.device_name,
                self.name,
                key,
                self.keypad.is_simulated()
            )
        )

        log(f"[KEYPAD] Key pressed: {key}")

        for subscriber in self._subscribers:
            subscriber(key)


