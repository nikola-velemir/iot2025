import paho.mqtt.client as mqtt
import time
import json

# Configuration
BROKER = "localhost"
PORT = 1883
BASE_TOPIC = "back_receive"


class MqttReceiver:
    def __init__(self, device_name, name):
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

        self.topic = f"{BASE_TOPIC}/{device_name}/{name}"
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print(f"Connected to Broker at {BROKER}")
            client.subscribe(self.topic)
            print(f"Subscribed to topic: {self.topic}")
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode("utf-8")
            print(f"New Message Received")
            print(f"Topic: {msg.topic}")
            print(f"Payload: {payload}")

            # Optional: If you expect JSON, parse it here
            # data = json.loads(payload)
            # print(f"Parsed Data: {data}")

        except Exception as e:
            print(f"Error processing message: {e}")

    def on_disconnect(self, client, userdata, flags, rc, properties):
        print("Disconnected from Broker")

    def start(self):
        try:
            print(f"Connecting to {BROKER}...")
            self.client.connect(BROKER, PORT, keepalive=60)

            self.client.loop_start()

        except KeyboardInterrupt:
            print("\nStopping client...")
            self.client.disconnect()
        except Exception as e:
            print(f"Could not connect: {e}")


if __name__ == "__main__":
    receiver = MqttReceiver("test","test")
    receiver.start()