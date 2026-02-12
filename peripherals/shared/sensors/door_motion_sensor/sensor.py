from shared.actuators.subscriber import Subscriber
from shared.logger.logger import log
from shared.mqtt.mqtt_data_point import MqttDataPoint
from shared.mqtt.mqtt_send import MqttBatchClient
from shared.sensors.door_motion_sensor.event import MotionStateChanged
from shared.sensors.door_motion_sensor.input import MotionInput


class DoorMotionSensor:
    def __init__(self, motion_input: MotionInput, name, device_name, mqtt_client):
        self.motion_input = motion_input
        self._last_state = None
        self._subscribers = []
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttBatchClient = mqtt_client

    def subscribe(self, subscriber: Subscriber):
        self._subscribers.append(subscriber.callback)

    def poll(self):
        motion = self.motion_input.is_motion()
        if motion != self._last_state:
            self._last_state = motion
            event = MotionStateChanged(motion_detected=motion)
            self.on_motion_change(event)

    def on_motion_change(self, event: MotionStateChanged):
        log("Motion detected!" if event.motion_detected else "No motion")

        self.mqtt_client.send(
            MqttDataPoint(
                "MotionSensor",
                self.device_name,
                self.name,
                event.motion_detected,
                self.motion_input.is_simulated()
            )
        )

        for subscriber in self._subscribers:
            subscriber(event)
