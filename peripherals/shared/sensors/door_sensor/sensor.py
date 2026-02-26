import threading

from shared.logger.logger import log
from shared.mqtt.back.send.alarm.mqtt_back_alarm_open_for_too_long import MqttBackAlarmOpenForTooLongPayload
from shared.mqtt.back.send.alarm.mqtt_back_door_closed_after_activation import MqttBackDoorClosedAfterActivation
from shared.mqtt.back.send.mqtt_back import MqttBackBatchClient
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.mqtt.influx.mqtt_telegraf_single_field_point import MqttTelegrafSingleFieldPoint
from shared.pubsub.publisher import Publisher
from shared.sensors.door_sensor.event import DoorStateChanged
from shared.sensors.door_sensor.input import ButtonInput


class DoorSensor(Publisher):
    def __init__(self, button: ButtonInput, name, device_name, mqtt_client):
        super().__init__()
        self.button = button
        self._last_state = None
        self.name = name
        self.device_name = device_name
        self.mqtt_client: MqttTelegrafBatchClient = mqtt_client
        self._timer = None
        self._lock = threading.Lock()
        self.mqtt_send_client = MqttBackBatchClient()

    def poll(self):
        is_closed = self.button.is_pressed()
        is_open = not is_closed

        if is_open != self._last_state:
            self._last_state = is_open

            event = DoorStateChanged(is_open=is_open)
            self.on_state_change(event)

    def on_state_change(self, event: DoorStateChanged):
        log("Door is OPEN" if event.is_open else "Door is CLOSED")

        self.mqtt_client.send(
            MqttTelegrafSingleFieldPoint(
                "DoorSensor",
                self.device_name,
                self.name,
                event.is_open,
                self.button.is_simulated()
            )
        )
        with self._lock:
            if event.is_open:
                self._start_monitoring()
            else:
                self._stop_monitoring()
                self.mqtt_send_client.send(MqttBackDoorClosedAfterActivation())

        self.notify(event)

    def _start_monitoring(self):
        if self._timer is not None:
            self._timer.cancel()
        log(f"[{self.name}] Door opened. Starting 5s monitor...")
        self._timer = threading.Timer(5.0, self._on_open_too_long)
        self._timer.start()

    def _stop_monitoring(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
            log(f"[{self.name}] Door closed within 5s. Monitor stopped.")

    def _on_open_too_long(self):
        with self._lock:
            self._monitor_timer = None
            log(f"[{self.name}] ALERT: Door has been open for more than 5 seconds!")

            event = MqttBackAlarmOpenForTooLongPayload()
            self.mqtt_send_client.send(event)
