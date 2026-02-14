from shared.mqtt.back.send.alarm.mqtt_back_alarm_gyro_payload import MqttBackAlarmGyroPayload
from shared.mqtt.back.send.mqtt_back import MqttBackBatchClient
from shared.mqtt.influx.mqtt_telegraf_multiple_field_gyro_point import MqttTelegrafMultipleGyroFieldPoint
from shared.sensors.gyroscope.input import GyroscopeInput


class GyroscopeSensor:
    def __init__(self, gyro_input: GyroscopeInput, name, device_name, mqtt_client,
                 threshold=0.2, report_all=False):
        self.gyro_input = gyro_input
        self.name = name
        self.device_name = device_name
        self.mqtt_client = mqtt_client
        self.threshold = threshold  # Ignore changes below this value
        self.report_all = report_all  # If True, always send to MQTT; if False, only send significant changes
        self._last_reported = (0.0, 0.0, 0.0)
        self._send_client = MqttBackBatchClient()

    def poll(self):
        x, y, z = self.gyro_input.read_gyro_data()

        # Apply threshold filter
        filtered_x = self._apply_threshold(x)
        filtered_y = self._apply_threshold(y)
        filtered_z = self._apply_threshold(z)

        if self._has_significant_change(filtered_x, filtered_y, filtered_z):
            print(f"[{self.name}]: x={filtered_x:.2f}, y={filtered_y:.2f}, z={filtered_z:.2f}")
            self.on_data_change(filtered_x, filtered_y, filtered_z)
            self._last_reported = (filtered_x, filtered_y, filtered_z)

        elif self.report_all:
            self.on_data_change(filtered_x, filtered_y, filtered_z)

    def _apply_threshold(self, value):
        return 0.0 if abs(value) < self.threshold else value

    def _has_significant_change(self, x, y, z):
        last_x, last_y, last_z = self._last_reported
        return (abs(x - last_x) > self.threshold or
                abs(y - last_y) > self.threshold or
                abs(z - last_z) > self.threshold)

    def on_data_change(self, x, y, z):
        self.mqtt_client.send(
            MqttTelegrafMultipleGyroFieldPoint(
                "GYRO",
                self.device_name,
                self.name,
                self.gyro_input.is_simulated(),
                x, y, z
            )
        )
        self._send_client.send(MqttBackAlarmGyroPayload("gyro"))