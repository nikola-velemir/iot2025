from logger.logger import log
from sensors.door_motion_sensor.event import MotionStateChanged
from sensors.door_motion_sensor.input import MotionInput


class DoorMotionSensor:
    def __init__(self, motion_input: MotionInput):
        self.motion_input = motion_input
        self._last_state = None
        self._subscribers = []

    def subscribe(self, handler):
        self._subscribers.append(handler)
    def poll(self):
        motion = self.motion_input.is_motion()
        if motion != self._last_state:
            self._last_state = motion
            event = MotionStateChanged(motion_detected=motion)
            self.on_motion_change(event)

    def on_motion_change(self, event: MotionStateChanged):
        log("Motion detected!" if event.motion_detected else "No motion")
        for subscriber in self._subscribers:
            subscriber(event)
