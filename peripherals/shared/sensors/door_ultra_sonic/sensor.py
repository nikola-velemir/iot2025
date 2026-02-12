from shared.logger.logger import log
from shared.mqtt.mqtt_data_point import MqttDataPoint
from shared.mqtt.mqtt_send import MqttBatchClient
from shared.sensors.door_ultra_sonic.input import UltrasonicInput


class UltrasonicSensor:
    def __init__(self, input_device: UltrasonicInput, name, device_name, mqtt_client):
        self.input_device = input_device
        self._last_distance = None
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttBatchClient = mqtt_client

    def poll(self):
        distance = self.input_device.read_distance()
        # only report if it changed significantly
        if self._last_distance is None or abs(distance - self._last_distance) > 0.05:
            self._last_distance = distance
            self.on_distance_change(distance)

    def on_distance_change(self, distance: float):
        self.mqtt_client.send(
            MqttDataPoint(
                "UltrasonicSensor",
                self.device_name,
                self.name,
                distance,
                self.input_device.is_simulated()
            )
        )

        log(f"{self.name} - Distance: {distance:.2f} m")
