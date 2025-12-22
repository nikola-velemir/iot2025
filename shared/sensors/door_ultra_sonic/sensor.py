from shared.logger.logger import log
from shared.sensors.door_ultra_sonic.input import UltrasonicInput


class UltrasonicSensor:
    def __init__(self, input_device: UltrasonicInput,name = "DUS1"):
        self.input_device = input_device
        self._last_distance = None
        self.name = name
    def poll(self):
        distance = self.input_device.read_distance()
        # only report if it changed significantly
        if self._last_distance is None or abs(distance - self._last_distance) > 0.05:
            self._last_distance = distance
            self.on_distance_change(distance)

    def on_distance_change(self, distance: float):
        log(f"{self.name} - Distance: {distance:.2f} m")
