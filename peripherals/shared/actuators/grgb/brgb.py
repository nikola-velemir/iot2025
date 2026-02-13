from shared.logger.logger import log
from shared.pubsub.subscriber import Subscriber


class BRGB(Subscriber):
    def __init__(self, name, mqtt_client):
        self.name = name
        self.mqtt_client = mqtt_client
        self.current_color = "OFF"

    def callback(self, event):
        log(f"[{self.name}] Actuator processing command: {event}")

        if event == "ON":
            self.turn_on()
        elif event == "OFF":
            self.turn_off()
        elif event in ["RED", "GREEN", "BLUE"]:
            self.set_color(event)

    def set_color(self, color):
        self.current_color = color
        log(f"{self.name} changed color to {color}")

    def turn_on(self):
        self.current_color = "WHITE"
        log(f"{self.name} turned ON")

    def turn_off(self):
        self.current_color = "OFF"
        log(f"🌑 {self.name} turned OFF")