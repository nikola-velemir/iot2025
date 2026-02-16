import threading

from shared.alarm.event import AlarmActivated, AlarmDeactivated
from shared.logger.logger import log
from shared.mqtt.back.receive.mqtt_back_receiver import MqttReceiver
from shared.pubsub.publisher import Publisher


class AlarmSystem(Publisher):
    def __init__(self, name, device_name, mqtt_client, subscribers):

        super().__init__()
        self.name = name
        self.device_name = device_name
        self._telegraf_client = mqtt_client

        self._timer = None
        self._arm_timer = None
        self._lock = threading.Lock()


        self.is_armed = False  #
        self.subscribe_multiple(subscribers)
        self._receive_client = MqttReceiver("alarm", self.message_cb)
        self._receive_client.start()

    def message_cb(self, topic, msg):
        print(msg)

        if "DEACTIVATE_ALARM" in msg:
            self.notify(AlarmDeactivated())
        elif "ACTIVATE_ALARM" in msg:
            self.notify(AlarmActivated())
    def _arm_system(self):
        with self._lock:
            self.is_armed = True
            self._arm_timer = None
            log("[SECURITY] SYSTEM ARMED! Monitoring doors...")
            self._report_alarm_state(False)

    def _deactivate_everything(self):
        self.is_armed = False
        self.is_alarm_active = False

        if self._arm_timer:
            self._arm_timer.cancel()
            self._arm_timer = None

        if self._timer:
            self._timer.cancel()
            self._timer = None

        log("[SECURITY] System fully deactivated.")
        self._report_alarm_state(False)

    def _report_alarm_state(self, active: bool):
       pass

