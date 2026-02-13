from shared.logger.logger import log
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.pubsub.publisher import Publisher
from shared.sensors.infra_red_sensor.input import IRInput


class IRSensor(Publisher):
    def __init__(self, ir_input: IRInput, name, device_name, mqtt_client):
        super().__init__()
        self.ir_input = ir_input
        self.name = name
        self.device_name = device_name
        self.mqtt_client = mqtt_client



    def poll(self):
        command = self.ir_input.read_key()

        if command:
            self.on_command_received(command)

    def on_command_received(self, command):
        log(f"[{self.name}] IR Command received: {command}")

        self.mqtt_client.send(
            MqttTelegrafPoint(
                "InfraredRemote",
                self.device_name,
                self.name,
                command,
                self.ir_input.is_simulated()
            )
        )

        self.notify(command)