from shared.actuators.buzzer.output import BuzzerOutput
from shared.alarm.event import AlarmActivated, AlarmDeactivated
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.pubsub.subscriber import Subscriber


class DoorBuzzerActuator(Subscriber):
    def __init__(self, buzzer: BuzzerOutput, name, device_name, mqtt_client):
        self.buzzer = buzzer
        self.name = name
        self.device_name = device_name
        self.telegraf_client: MqttTelegrafBatchClient = mqtt_client

    def callback(self, event):
        is_on = False
        if isinstance(event, AlarmActivated):
            self.buzzer.on()
            is_on = True
        if isinstance(event, AlarmDeactivated):
            self.buzzer.off()
            is_on = False

        self.telegraf_client.send(
            MqttTelegrafPoint(
                "BuzzerActuator",
                self.device_name,
                self.name,
                is_on,
                self.buzzer.is_simulated()
            )
        )