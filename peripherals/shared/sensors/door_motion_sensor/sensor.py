from shared.logger.logger import log
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
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


    def poll(self):
        motion = self.motion_input.is_motion()
        if motion != self._last_state:
            self._last_state = motion
            event = MotionStateChanged(motion_detected=motion)
            self.on_motion_change(event)

    def on_motion_change(self, event: MotionStateChanged):
        log("Motion detected!" if event.motion_detected else "No motion")

        self.mqtt_client.send(
            MqttTelegrafPoint(
                "MotionSensor",
                self.device_name,
                self.name,
                event.motion_detected,
                self.motion_input.is_simulated()
            )
        )
        self.notify(event)
