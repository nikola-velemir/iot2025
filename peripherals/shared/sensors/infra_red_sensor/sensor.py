from shared.logger.logger import log
from shared.mqtt.influx.mqtt_telegraf_single_field_point import MqttTelegrafSingleFieldPoint
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
            MqttTelegrafSingleFieldPoint(
                "InfraredRemote",
                self.device_name,
                self.name,
                command,
                self.ir_input.is_simulated()
            )
        )
        delegated_command = ""
        if command == "1":
            delegated_command = "RED"
        elif command == "2":
            delegated_command = "GREEN"
        elif command == "3":
            delegated_command = "BLUE"
        elif command == "4":
            delegated_command = "YELLOW"
        elif command == "5":
            delegated_command = "PURPLE"
        elif command == "6":
            delegated_command = "CYAN"
        elif command == "7":
            delegated_command = "WHITE"
        elif command == "OK":
            delegated_command = "ON"
        elif command == "0":
            delegated_command = "OFF"
        if delegated_command != "":
            self.notify(delegated_command)
