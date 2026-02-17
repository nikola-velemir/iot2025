from shared.logger.logger import log
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.mqtt.influx.mqtt_telegraf_single_field_point import MqttTelegrafSingleFieldPoint
from shared.pubsub.publisher import Publisher
from shared.sensors.button.event import ButtonEvent
from shared.sensors.door_sensor.input import ButtonInput


class Button(Publisher):
    def __init__(self, button: ButtonInput, full_name, name, device_name, mqtt_client):
        super().__init__()
        self.button = button
        self._last_state = False  # start as not pressed
        self.name = name
        self.full_name = full_name
        self.device_name = device_name
        self.mqtt_client: MqttTelegrafBatchClient = mqtt_client

    def poll(self):
        is_pressed = self.button.is_pressed()  # True if pressed

        # Trigger only when transitioning from not pressed → pressed
        if is_pressed and not self._last_state:
            self._last_state = True  # update state
            event = ButtonEvent("PRESSED")
            self.on_state_change(event)
        elif not is_pressed:
            self._last_state = False  # update when released

    def on_state_change(self, event: ButtonEvent):
        log(f"{self.full_name} is pressed")

        self.mqtt_client.send(
            MqttTelegrafSingleFieldPoint(
                "Button",
                self.device_name,
                self.name,
                True,
                self.button.is_simulated()
            )
        )

        self.notify(event)
