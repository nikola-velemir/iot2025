from shared.logger.logger import log
from shared.sensors.door_sensor.event import DoorStateChanged
from shared.actuators.door_light.input import LightInput


class DoorLightSensor(object):
    def __init__(self, light: LightInput, name: str = "DL1"):
        self.light = light
        self._last_state = None
        self.name = name

    def handle_door_event(self,event:DoorStateChanged):
        if event.is_open:
            self.light.turn_on()
        else:
            self.light.turn_off()
        self.on_state_change(event.is_open)
    def on_state_change(self, is_light: bool):
        log(
            self.name + ": " +
            "Light is ON" if is_light else "Light is OFF"
        )
    def poll(self):
        """Optional: just report current state."""
        current_state = self.light.is_light()
        if current_state != self._last_state:
            self._last_state = current_state
            self.on_state_change(current_state)