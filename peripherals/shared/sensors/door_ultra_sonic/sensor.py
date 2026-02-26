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

    def get_direction(self, lookback_seconds=2.0):
        now = time.time()

        # keep recent values only
        relevant = [(t, d) for t, d in self.history if now - t <= lookback_seconds]

        if len(relevant) < 5:
            return "Unknown"

        # --- 1. Median smoothing (last 5 samples) ---
        distances = [d for _, d in relevant]
        window = 5
        smoothed = []

        for i in range(len(distances) - window + 1):
            slice_ = distances[i:i + window]
            smoothed.append(sorted(slice_)[window // 2])

        if len(smoothed) < 3:
            return "Unknown"

        # --- 2. Compute slopes between consecutive values ---
        slopes = [smoothed[i] - smoothed[i - 1] for i in range(1, len(smoothed))]

        # --- 3. Ignore tiny noise ---
        movement_threshold = 1.5  # cm
        slopes = [s for s in slopes if abs(s) > 0.5]

        if len(slopes) < 3:
            return "Unknown"

        # --- 4. Majority vote direction ---
        positive = sum(1 for s in slopes if s > 0)
        negative = sum(1 for s in slopes if s < 0)

        total_movement = smoothed[0] - smoothed[-1]

        if negative > positive and total_movement > movement_threshold:
            return "Entering"

        if positive > negative and total_movement < -movement_threshold:
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

        #log(f"{self.name} - Distance: {distance:.2f} cm")
