import threading
import time

from shared.actuators.lcd.output import LcdOutput
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.pubsub.subscriber import Subscriber


class LcdActuator(Subscriber):
    def __init__(self, lcd: LcdOutput, name, device_name, mqtt_client, is_simulated = True):
        self.lcd = lcd
        self.name = name
        self.device_name = device_name

        self.telegraf_client = mqtt_client
        self.sensor_data = {}
        self._lock = threading.Lock()
        self.is_simulated = is_simulated
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
            sensors = list(self.sensor_data.keys())
            if not sensors:
                self.lcd.display_text("Waiting for", "sensor data...")
                time.sleep(2)
                continue

            for sensor_id in sensors:
                with self._lock:
                    data = self.sensor_data.get(sensor_id)

                if data:
                    line1 = f"Sensor: {sensor_id}"
                    line2 = f"T:{data['temp']}C H:{data['hum']}%"
                    self.lcd.display_text(line1, line2)

                    self.telegraf_client.send(
                        MqttTelegrafPoint(
                            "LCD",  # promeni na tip
                            self.device_name,
                            self.name,
                            line1 + " " + line2,
                            self.is_simulated
                        )
                    )
                time.sleep(5)

    def on_state_change(self, message: str):
        pass