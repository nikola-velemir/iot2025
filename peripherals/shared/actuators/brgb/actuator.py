from paho.mqtt.subscribe import callback

from shared.logger.logger import log
from shared.mqtt.back.receive.mqtt_back_receiver import MqttReceiver
from shared.mqtt.influx.mqtt_telegraf_point import MqttTelegrafPoint
from shared.pubsub.subscriber import Subscriber


class BRGB(Subscriber):
    def __init__(self, output, name, device_name, mqtt_client):
        self.output = output
        self.name = name
        self.telegraf_client = mqtt_client
        self.device_name = device_name
        self.current_color = "OFF"
        self.receive_client = MqttReceiver("brgb", self.msg_callback)
        self.receive_client.start()

    def msg_callback(self, topic, payload):
        if "BRGB_NEW_LIGHT" in payload:
            color_event = payload.split(":")[-1]
            self._handle_color_change(color_event)

    def _handle_color_change(self, event):
        log(f"[{self.name}] Actuator processing command: {event}")

        if event == "ON":
            self.turn_on()
        elif event == "OFF":
            self.turn_off()
        else:
            self.set_color(event)
    def callback(self, event):
       self._handle_color_change(event)

    def set_color(self, color):
        self.current_color = color
        log(f"{self.name} changed color to {color}")

    def turn_on(self):
        self.current_color = "WHITE"
        log(f"{self.name} turned ON")
        self.telegraf_client.send(
            MqttTelegrafPoint(
                "BRGB",
                self.device_name,
                self.name,
                1,
                self.output.is_simulated()
            )
        )

    def turn_off(self):
        self.current_color = "OFF"
        log(f"🌑 {self.name} turned OFF")
        self.telegraf_client.send(
            MqttTelegrafPoint(
                "BRGB",
                self.device_name,
                self.name,
                0,
                self.output.is_simulated()
            )
        )