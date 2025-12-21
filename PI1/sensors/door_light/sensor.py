from logger.logger import log
from sensors.door_sensor.event import DoorStateChanged
from sensors.door_light.input import LightInput


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
