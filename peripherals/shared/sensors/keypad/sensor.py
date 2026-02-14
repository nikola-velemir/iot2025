from copy import deepcopy

from shared.mqtt.back.send.alarm.mqtt_back_alarm_arm_payload import MqttBackAlarmArmPayload
from shared.mqtt.back.send.mqtt_back import MqttBackBatchClient
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.mqtt.influx.mqtt_telegraf_single_field_point import MqttTelegrafSingleFieldPoint
from shared.pubsub.subscriber import Subscriber
from shared.sensors.keypad.input import KeypadInput
from shared.logger.logger import log


class KeyPad:
    def __init__(self, keypad: KeypadInput, name, device_name, mqtt_client):
        self.keypad = keypad
        self._subscribers = []
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttTelegrafBatchClient = mqtt_client
        self._current_input_pint = ""
        self.mqtt_send_client = MqttBackBatchClient()

    def subscribe(self, subscriber: Subscriber):
        self._subscribers.append(subscriber.callback)

    def poll(self):
        key = self.keypad.read_key()
        if key:
            self.on_key_pressed(key)

    def on_key_pressed(self, key: str):
        self.mqtt_client.send(
            MqttTelegrafSingleFieldPoint(
                "KeypadSensor",
                self.device_name,
                self.name,
                key,
                self.keypad.is_simulated()
            )
        )

        log(f"[KEYPAD] Key pressed: {key}")
        self._current_input_pint += key
        if len(self._current_input_pint) == 4:
            print("POKUSAJ ARMOVANJA")
            self.mqtt_send_client.send(MqttBackAlarmArmPayload(deepcopy(self._current_input_pint)))
            self._current_input_pint = ""
