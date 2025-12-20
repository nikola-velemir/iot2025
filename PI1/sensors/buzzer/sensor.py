from sensors.buzzer.output import BuzzerOutput
from sensors.door_motion_sensor.event import MotionStateChanged


class DoorBuzzer:
    def __init__(self, buzzer: BuzzerOutput):
        self.buzzer = buzzer

    def handle_motion_event(self, event: MotionStateChanged):
        if event.motion_detected:
            self.buzzer.on()
        else:
            self.buzzer.off()