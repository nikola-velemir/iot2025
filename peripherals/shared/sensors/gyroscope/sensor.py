from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.sensors.gyroscope.input import GyroscopeInput


class GyroscopeSensor:
    def __init__(self, gyro_input: GyroscopeInput, name, device_name, mqtt_client):
        self.gyro_input = gyro_input
        self.name = name
        self.device_name = device_name
        self.mqtt_client = mqtt_client

    def poll(self):
        x, y, z = self.gyro_input.read_gyro_data()
        print(f"[{self.name}]:", x, y, z)
        self.on_data_change(x, y, z)

    def on_data_change(self, x, y, z):
         for axis, value in [("gyro_x", x), ("gyro_y", y), ("gyro_z", z)]:
            self.mqtt_client.send(
                MqttTelegrafPoint(
                    axis,
                    self.device_name,
                    self.name,
                    value,
                    self.gyro_input.is_simulated()
                )
            )