from shared.logger.logger import log
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.sensors.dht_sensor.input import DHTInput


class DHTSensor:
    def __init__(self, dht_input: DHTInput, name, device_name, mqtt_client):
        self.dht_input = dht_input
        self.name = name
        self.device_name = device_name
        self.mqtt_client = mqtt_client
        self._last_temp = None
        self._last_hum = None

    def poll(self):
        temp, hum = self.dht_input.read_data()

        # Only send update if values changed significantly (e.g., by 0.1)
        if temp != self._last_temp or hum != self._last_hum:
            self._last_temp = temp
            self._last_hum = hum
            self.on_data_change(temp, hum)

    def on_data_change(self, temp, hum):
        log(f"[{self.name}] Temp: {temp}°C, Hum: {hum}%")

        # Sending Temperature
        self.mqtt_client.send(
            MqttTelegrafPoint("Temperature", self.device_name, self.name, temp, self.dht_input.is_simulated())
        )
        # Sending Humidity
        self.mqtt_client.send(
            MqttTelegrafPoint("Humidity", self.device_name, self.name, hum, self.dht_input.is_simulated())
        )