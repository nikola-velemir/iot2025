from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint


class MqttTelegrafSingleFieldPoint(MqttTelegrafPoint):
    def __init__(self, type_name, device_name, name, value, is_simulated):
        super().__init__(type_name, device_name, name, is_simulated)
        self.value = value

    def get_value(self):
        return { "value": self.value }