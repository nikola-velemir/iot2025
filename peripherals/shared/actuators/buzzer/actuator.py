from shared.actuators.buzzer.output import BuzzerOutput
from shared.actuators.subscriber import Subscriber
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.sensors.door_motion_sensor.event import MotionStateChanged


class DoorBuzzerActuator(Subscriber):
    def __init__(self, buzzer: BuzzerOutput, name, device_name, mqtt_client):
        self.buzzer = buzzer
        self.name = name
        self.device_name = device_name
        self.telegraf_client: MqttTelegrafBatchClient = mqtt_client

    def callback(self, event):
        if not isinstance(event, MotionStateChanged):
            return

        if event.motion_detected:
            self.buzzer.on()
        else:
            self.buzzer.off()

        self.telegraf_client.send(
            MqttTelegrafPoint(
                "BuzzerActuator",
                self.device_name,
                self.name,
                event.motion_detected,
                self.buzzer.is_simulated()
            )
        )