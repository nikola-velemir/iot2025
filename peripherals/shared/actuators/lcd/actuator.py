import threading
import time

from shared.actuators.lcd.output import LcdOutput
from shared.mqtt.influx.mqtt_telegraf_single_field_point import MqttTelegrafSingleFieldPoint
from shared.pubsub.subscriber import Subscriber


class LcdActuator(Subscriber):
    def __init__(self, lcd: LcdOutput, name, device_name, mqtt_client):
        self.output = lcd
        self.name = name
        self.device_name = device_name
        self._last_render = None

        self.telegraf_client = mqtt_client
        self.sensor_data = {}
        self._lock = threading.Lock()
        self.display_thread = threading.Thread(target=self._rotation_loop, daemon=True)
        self.display_thread.start()

    def callback(self, event):
        if hasattr(event, 'temp') and hasattr(event, 'sensor_name'):
            with self._lock:
                self.sensor_data[event.sensor_name] = {
                    "temp": event.temp,
                    "hum": event.humidity
                }

    def _rotation_loop(self):
        while True:
            with self._lock:
                snapshot = dict(self.sensor_data)

            if not snapshot:
                self._render_if_changed("Waiting for", "sensor data...")
                time.sleep(2)
                continue

            for sensor_id, data in snapshot.items():
                line1 = f"Sensor: {sensor_id}"
                line2 = f"T:{data['temp']}C H:{data['hum']}%"

                self._render_if_changed(line1, line2)

                self.telegraf_client.send(
                    MqttTelegrafSingleFieldPoint(
                        "LCD",
                        self.device_name,
                        self.name,
                        line1 + " " + line2,
                        self.output.is_simulated()
                    )
                )

                time.sleep(5)

    def _render_if_changed(self, line1, line2):
        content = (line1, line2)
        if content != self._last_render:
            self.output.display_text(line1, line2)
            self._last_render = content

    def on_state_change(self, message: str):
        pass