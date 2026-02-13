from shared.logger.logger import log
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.pubsub.publisher import Publisher
from shared.sensors.door_sensor.event import DoorStateChanged
from shared.sensors.door_sensor.input import ButtonInput


class DoorSensor(Publisher):
    def __init__(self, button: ButtonInput, name, device_name, mqtt_client):
        super().__init__()
        self.button = button
        self._last_state = None
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttTelegrafBatchClient = mqtt_client

    def poll(self):
        is_closed = self.button.is_pressed()
        is_open = not is_closed

        if is_open != self._last_state:
            self._last_state = is_open

            event = DoorStateChanged(is_open=is_open)
            self.on_state_change(event)

    def on_state_change(self, event: DoorStateChanged):
        log("Door is OPEN" if event.is_open else "Door is CLOSED")

        self.mqtt_client.send(
            MqttTelegrafPoint(
                "DoorSensor",
                self.device_name,
                self.name,
                event.is_open,
                self.button.is_simulated()
            )
        )

        self.notify(event)
