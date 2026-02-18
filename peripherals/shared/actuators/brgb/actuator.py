from shared.logger.logger import log
from shared.mqtt.back.receive.mqtt_back_receiver import MqttReceiver
from shared.mqtt.influx.mqtt_telegraf_single_field_point import MqttTelegrafSingleFieldPoint
from shared.pubsub.subscriber import Subscriber


class BRGB(Subscriber):
    def __init__(self, output, name, device_name, mqtt_client):
        self.output = output
        self.name = name
        self._telegraf_client = mqtt_client
        self.device_name = device_name

        self._is_on = False
        self._current_color = "WHITE"
        self._receive_client = MqttReceiver("brgb", self.msg_callback)
        self._receive_client.start()


    def msg_callback(self, topic, payload):
        if "BRGB_NEW_LIGHT" in payload:
            color_event = payload.split(":")[-1]
            self._handle_color_change(color_event)

    def _handle_color_change(self, event):
        log(f"[{self.name}] Actuator processing command: {event}")

        if event == "ON":

            self.turn_on()
            self.set_color("WHITE")
        elif event == "OFF":
            self.turn_off()
        else:
            if not self._is_on:
                self.turn_on()
            self.set_color(event)
    def callback(self, event):
       self._handle_color_change(event)

    def set_color(self, color):
        self.current_color = color
        log(f"{self.name} changed color to {color}")
        self.output.set_color(color)

    def turn_on(self):
        self.output.turn_on()
        self.current_color = "WHITE"
        self.set_color("WHITE")
        log(f"{self.name} turned ON")
        self._is_on = True
        self.telegraf_client.send(
            MqttTelegrafSingleFieldPoint(
                "BRGB",
                self.device_name,
                self.name,
                True,
                self.output.is_simulated()
            )
        )

    def turn_off(self):
        self.output.turn_off()
        self.current_color = "OFF"
        self._is_on = False
        log(f"🌑 {self.name} turned OFF")
        self.telegraf_client.send(
            MqttTelegrafSingleFieldPoint(
                "BRGB",
                self.device_name,
                self.name,
                False,
                self.output.is_simulated()
            )
        )