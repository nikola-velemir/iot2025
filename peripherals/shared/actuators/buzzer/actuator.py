from shared.actuators.buzzer.output import BuzzerOutput
from shared.actuators.subscriber import Subscriber
from shared.mqtt.mqtt_data_point import MqttDataPoint
from shared.mqtt.mqtt_send import MqttBatchClient
from shared.sensors.door_motion_sensor.event import MotionStateChanged


class DoorBuzzerActuator(Subscriber):
    def __init__(self, buzzer: BuzzerOutput, name, device_name, mqtt_client):
        self.buzzer = buzzer
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttBatchClient = mqtt_client

    def callback(self, event):
        if not isinstance(event, MotionStateChanged):
            return

        if event.motion_detected:
            self.buzzer.on()
        else:
            self.buzzer.off()

        self.mqtt_client.send(
            MqttDataPoint(
                "BuzzerActuator",
                self.device_name,
                self.name,
                event.motion_detected,
                self.buzzer.is_simulated()
            )
        )