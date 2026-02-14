from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint


class MqttTelegrafMultipleGyroFieldPoint(MqttTelegrafPoint):
    def __init__(self, type_name, device_name, name, is_simulated, val_x, val_y, val_z):
        super().__init__(type_name, device_name, name, is_simulated)
        self.val_x = val_x
        self.val_y = val_y
        self.val_z = val_z

    def get_value(self):
        return {
            "value_x": self.val_x,
            "value_y": self.val_y,
            "value_z": self.val_z,
        }