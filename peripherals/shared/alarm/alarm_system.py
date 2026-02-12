import threading

from shared.actuators.subscriber import Subscriber
from shared.alarm.event import AlarmActivated, AlarmDeactivated
from shared.logger.logger import log
from shared.sensors.door_sensor.event import DoorStateChanged


class AlarmSystem(Subscriber):
    def __init__(self, name, device_name, mqtt_client, subscribers):

        self.name = name
        self.device_name = device_name
        self.mqtt_client = mqtt_client

        self._timer = None
        self._arm_timer = None
        self._lock = threading.Lock()

        self.current_input = ""
        self.correct_pin = "1234"

        self.is_armed = False  #
        self.is_alarm_active = False  # Zujalica trenutno zvoni
        self.subscribers = []
        [self.subscribe(s) for s in subscribers]
    def subscribe(self, subscriber: Subscriber):
        self.subscribers.append(subscriber.callback)
    def callback(self, event):
        with self._lock:
            if isinstance(event, str):
                self._handle_key_pad(event)
            elif isinstance(event, DoorStateChanged):
                self._handle_door(event)

    def _handle_key_pad(self, key):
        self.current_input += key
        log(f"[SECURITY] Key pressed. Current buffer length: {len(self.current_input)}")

        if len(self.current_input) == 4:
            if self.current_input == self.correct_pin:
                log("[SECURITY] Correct PIN entered.")
                self._on_correct_pin()
            else:
                log("[SECURITY] Wrong PIN entered!")
            self.current_input = ""

    def _on_correct_pin(self):
        if self.is_alarm_active or self.is_armed or self._arm_timer:
            log("[SECURITY] Disarming system and stopping alarm.")
            self._deactivate_everything()
        else:
            log("[SECURITY] Arming system in 10 seconds...")
            if self._arm_timer: self._arm_timer.cancel()
            self._arm_timer = threading.Timer(10.0, self._arm_system)
            self._arm_timer.start()

    def _arm_system(self):
        with self._lock:
            self.is_armed = True
            self._arm_timer = None
            log("[SECURITY] SYSTEM ARMED! Monitoring doors...")
            self._report_alarm_state(False)  # Šalje status na MQTT/Influx

    def _handle_door(self, event):
        if not self.is_armed:
            return

        if event.is_open:
            self._start_monitoring()
        else:
            self._stop_alarm_and_monitoring()

    def _start_monitoring(self):
        if self._timer is not None:
            self._timer.cancel()

        log(f"{self.name}: Door opened while armed. Alarm in 5s if not closed.")
        self._timer = threading.Timer(5.0, self._activate_alarm)
        self._timer.start()

    def _activate_alarm(self):
        with self._lock:
            self.is_alarm_active = True
            self.notify(AlarmActivated())
            log(f"ALARM ACTIVATED! {self.name} open too long!")
            self._report_alarm_state(True)

    def _stop_alarm_and_monitoring(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        if self.is_alarm_active:
            self.notify(AlarmDeactivated())
            self.is_alarm_active = False
            log(f"{self.name}: Door closed, alarm deactivated.")
            self._report_alarm_state(False)
        else:
            log(f"{self.name}: Door closed safely within 5s.")

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

    def notify(self,event):
        for sub in self.subscribers:
            sub(event)