import time

from shared.logger.logger import log
from shared.mqtt.back.send.alarm.mqtt_back_alarm_motion_payload import MqttBackAlarmMotionPayload
from shared.mqtt.back.send.mqtt_back import MqttBackBatchClient
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.mqtt.influx.mqtt_telegraf_single_field_point import MqttTelegrafSingleFieldPoint
from shared.pubsub.publisher import Publisher
from shared.sensors.door_motion_sensor.event import MotionStateChanged
from shared.sensors.door_motion_sensor.input import MotionInput


class DoorMotionSensor(Publisher):
    def __init__(self, motion_input: MotionInput, name, device_name, mqtt_client):
        super().__init__()
        self.motion_input = motion_input
        self._last_state = None
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttTelegrafBatchClient = mqtt_client
        self.send_client = MqttBackBatchClient()

        self._candidate_state = None
        self._candidate_since = None
        self.debounce_time = 0.5  # seconds

    def poll(self):
        now = time.monotonic()
        current = self.motion_input.is_motion()

        if current != self._candidate_state:
            self._candidate_state = current
            self._candidate_since = now
            return

        if current != self._last_state:
            if now - self._candidate_since >= self.debounce_time:
                self._last_state = current
                event = MotionStateChanged(motion_detected=current)
                self.on_motion_change(event)

    def on_motion_change(self, event: MotionStateChanged):
        log("Motion detected!" if event.motion_detected else "No motion")

        self.mqtt_client.send(
            MqttTelegrafSingleFieldPoint(
                "MotionSensor",
                self.device_name,
                self.name,
                event.motion_detected,
                self.motion_input.is_simulated()
            )
        )
        if event.motion_detected:
            self.send_client.send(MqttBackAlarmMotionPayload("motion_sensor"))
            self.notify(event)
