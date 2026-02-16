import json
import time
import threading
from queue import Queue, Empty
import paho.mqtt.client as mqtt

from shared.mqtt.back.send.alarm.mqtt_back_alarm_arm_payload import MqttBackAlarmArmPayload
from shared.mqtt.back.send.alarm.mqtt_back_alarm_door_person_event_payload import MqttBackAlarmDoorPersonEventPayload
from shared.mqtt.back.send.alarm.mqtt_back_alarm_gyro_payload import MqttBackAlarmGyroPayload
from shared.mqtt.back.send.alarm.mqtt_back_alarm_motion_payload import MqttBackAlarmMotionPayload
from shared.mqtt.back.send.mqtt_back_send_payload import MqttBackSendPayload

BROKER = "192.168.0.3"
PORT = 1883
TOPIC = "test/topic"


class MqttBackBatchClient:
    def __init__(self, batch_size=10, flush_interval=5.0):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.queue = Queue()

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self._on_connect

        self.client.connect(BROKER, PORT, keepalive=60)
        self.client.loop_start()

        self.running = True
        self.worker_thread = threading.Thread(target=self._batch_worker, daemon=True)
        self.worker_thread.start()

    @staticmethod
    def _on_connect(_client, _userdata, _flags, rc, _properties=None):
        if rc == 0:
            print(f"Connected to {BROKER}")
        else:
            print(f"Connection failed: {rc}")

    def send(self, payload: MqttBackSendPayload):
        self.queue.put(payload)

    def _batch_worker(self):
        batch = []
        last_flush = time.time()

        while self.running:
            try:
                item = self.queue.get(timeout=0.1)
                batch.append(item)
            except Empty:
                pass

            current_time = time.time()
            if len(batch) >= self.batch_size or (len(batch) > 0 and (current_time - last_flush) > self.flush_interval):
                self._flush(batch)
                batch = []
                last_flush = current_time

    def _flush(self, batch):
        for data_point in batch:
            dynamic_topic = data_point.topic

            payload = json.dumps(data_point.get_payload_as_dict())
            self.client.publish(dynamic_topic, payload=payload, qos=1)

        print(f"Flushed {len(batch)} points to their respective topics (back end).")

    def stop(self):
        self.running = False
        self.worker_thread.join()
        remaining = []
        while not self.queue.empty():
            remaining.append(self.queue.get())
        if remaining:
            self._flush(remaining)

        self.client.loop_stop()
        self.client.disconnect()


if __name__ == "__main__":
    mqtt_service = MqttBackBatchClient(batch_size=10, flush_interval=5.0)

    try:
        print("Sending 100 messages rapidly...")
        for i in range(100):
            mqtt_service.send(MqttBackAlarmArmPayload("1234"))
            mqtt_service.send(MqttBackAlarmDoorPersonEventPayload("left"))
            mqtt_service.send(MqttBackAlarmMotionPayload(123))
            mqtt_service.send(MqttBackAlarmMotionPayload("yes"))
            mqtt_service.send(MqttBackAlarmGyroPayload("yes"))
            time.sleep(0.5)

        print("Waiting for final time-based flush...")
        time.sleep(10)

    except KeyboardInterrupt:
        pass
    finally:
        mqtt_service.stop()
