import threading

from shared.subscriber.subscriber import Subscriber
from shared.logger.logger import log
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.sensors.door_motion_sensor.event import MotionStateChanged
from shared.actuators.door_light.output import LightOutput


class DoorLightActuator(Subscriber):
    def __init__(self, light: LightOutput, name, device_name, mqtt_client):
        self.light = light
        self._last_state = None
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttTelegrafBatchClient = mqtt_client
        self._timer = None  # Tajmer za automatsko gašenje

    def callback(self, event):
        if not isinstance(event, MotionStateChanged):
            return

        if not event.motion_detected:
            return

        if self._timer:
            self._timer.cancel()

        self._switch_light(True)

        # Pokreni tajmer koji će ugasiti svetlo nakon 10 sekundi
        self._timer = threading.Timer(10.0, self._switch_light, [False])
        self._timer.start()

    def _switch_light(self, state: bool):
        if state:
            self.light.turn_on()
        else:
            self.light.turn_off()
        self.on_state_change(state)
    def poll(self):
        """Optional: just report current state."""
        current_state = self.light.is_light()
        if current_state != self._last_state:
            self._last_state = current_state
            self.on_state_change(current_state)

    def on_state_change(self, is_light: bool):
        self.mqtt_client.send(
            MqttTelegrafPoint(
                "LightActuator",
                self.device_name,
                self.name,
                is_light,
                self.light.is_simulated()
            )
        )

        log(
            self.name + ": " +
            "Light is ON" if is_light else "Light is OFF"
        )