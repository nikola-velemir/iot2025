import time
from collections import deque

from shared.logger.logger import log
from shared.mqtt.back.send.alarm.mqtt_back_alarm_door_person_event_payload import MqttBackAlarmDoorPersonEventPayload
from shared.mqtt.back.send.mqtt_back import MqttBackBatchClient
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.mqtt.influx.mqtt_telegraf_single_field_point import MqttTelegrafSingleFieldPoint
from shared.pubsub.subscriber import Subscriber
from shared.sensors.door_motion_sensor.event import MotionStateChanged
from shared.sensors.door_ultra_sonic.input import UltrasonicInput



class UltrasonicSensor(Subscriber):

    def __init__(self, input_device: UltrasonicInput, name, device_name, mqtt_client):
        self.input_device = input_device
        self._last_distance = None
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttTelegrafBatchClient = mqtt_client
        self.history = deque(maxlen=50)
        self.send_client = MqttBackBatchClient()
    def callback(self, event):
        if not isinstance(event, MotionStateChanged):
            return
        direction = self.get_direction()
        if direction == "Entering":
            print("Person entering")
            # send that person entered on back
            self.send_client.send(MqttBackAlarmDoorPersonEventPayload("entered"))

        if direction == "Exiting":
            print("Person exiting")
            self.send_client.send(MqttBackAlarmDoorPersonEventPayload("left"))

    def poll(self):
        distance = self.input_device.read_distance()
        current_time = time.time()
        self.history.append((current_time, distance))
        # only report if it changed significantly
        if self._last_distance is None or abs(distance - self._last_distance) > 0.05:
            self._last_distance = distance
            self.on_distance_change(distance)

    def get_direction(self, lookback_seconds=3.0):
        now = time.time()
        relevant_measurements = [d for t, d in self.history if now - t <= lookback_seconds]

        if len(relevant_measurements) < 2:
            return "Unknown"

        first = relevant_measurements[0]
        last = relevant_measurements[-1]
        diff = first - last

        if diff > 0.1:
            return "Entering"
        elif diff < -0.1:
            return "Exiting"

        return "Stationary/Unknown"
    def on_distance_change(self, distance: float):
        self.mqtt_client.send(
            MqttTelegrafSingleFieldPoint(
                "UltrasonicSensor",
                self.device_name,
                self.name,
                distance,
                self.input_device.is_simulated()
            )
        )

        log(f"{self.name} - Distance: {distance:.2f} m")
