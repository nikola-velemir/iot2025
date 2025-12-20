from sensors.door_sensor.event import DoorStateChanged
from sensors.door_sensor.input import ButtonInput


class DoorSensor(object):
    def __init__(self, button:ButtonInput,name = "DS1"):
        self.button = button
        self._last_state = None
        self.name = name
        self._subscribers = []

    def subscribe(self, callback):
        self._subscribers.append(callback)

    def poll(self):
        is_closed = self.button.is_pressed()
        is_open = not is_closed

        if is_open != self._last_state:
            self._last_state = is_open

            event = DoorStateChanged(is_open=is_open)
            self.on_state_change(event)

    def on_state_change(self, event:DoorStateChanged):
        print("Door is OPEN" if event.is_open else "Door is CLOSED")

        for subscriber in self._subscribers:
            subscriber(event)
