import threading

from shared.actuators.stopwatch.output import TimerOutput
from shared.logger.logger import log
from shared.mqtt.back.receive.mqtt_back_receiver import MqttReceiver
from shared.mqtt.influx.mqtt_telegraf_single_field_point import MqttTelegrafSingleFieldPoint
from shared.pubsub.subscriber import Subscriber
from shared.sensors.button.event import ButtonEvent


class KitchenStopwatch(Subscriber):
    def __init__(self, output: TimerOutput, name, device_name, mqtt_client, add_seconds=60):
        self.output = output
        self.name = name
        self.device_name = device_name
        self.mqtt_client = mqtt_client
        self.add_seconds = add_seconds

        self._remaining_seconds = 0
        self._is_running = False
        self._is_blinking = False
        self._timer_thread = None
        self._blink_thread = None
        self._lock = threading.Lock()
        self._receive_client = MqttReceiver("stopwatch",self.configure_stopwatch)
        self._receive_client.start()

    def configure_stopwatch(self,topic, payload):
        if "STOPWATCH_STARTED" in payload:
            time_payload = payload.split(":")[-1]
            set_time, n_seconds = time_payload.split(",")
            self.set_time(int(set_time))
            self.add_seconds = int(n_seconds)
            print("Set config from web")

    def callback(self, event):
        with self._lock:
            if isinstance(event, ButtonEvent) and event.state == "PRESSED":
                self._handle_button_press()

    def set_time(self, seconds: int):
        with self._lock:
            if self._is_blinking:
                self._stop_blinking()
                self._remaining_seconds = 0
                self._update_display()
                log(f"[{self.name}] Timer reset from blinking state")
                return

            self._remaining_seconds = seconds
            self._is_running = False

            if self._timer_thread:
                self._timer_thread.cancel()
                self._timer_thread = None

            self._update_display()
            log(f"[{self.name}] Timer set to {seconds}s ({self._format_time(seconds)})")

    def start(self):
        with self._lock:
            if self._remaining_seconds <= 0:
                log(f"[{self.name}] Cannot start - no time set")
                return

            if self._is_running:
                log(f"[{self.name}] Timer already running")
                return

            self._is_running = True
            log(f"[{self.name}] Timer started")
            self._schedule_tick()

    def stop(self):
        with self._lock:
            self._is_running = False
            if self._timer_thread:
                self._timer_thread.cancel()
                self._timer_thread = None
            log(f"[{self.name}] Timer stopped")

    def _handle_button_press(self):
        if self._is_blinking:
            self._stop_blinking()
            self._remaining_seconds = 0
            self._update_display()
            log(f"[{self.name}] Blinking stopped by button")
        else:
            self._remaining_seconds += self.add_seconds
            log(f"[{self.name}] Added {self.add_seconds}s. New time: {self._format_time(self._remaining_seconds)}")
            self._update_display()

            if not self._is_running and self._remaining_seconds > 0:
                self._is_running = True
                log(f"[{self.name}] Timer started")
                self._schedule_tick()

    def _schedule_tick(self):
        """Schedule next timer tick"""
        if self._is_running:
            self._timer_thread = threading.Timer(1.0, self._tick)
            self._timer_thread.start()

    def _tick(self):
        with self._lock:
            if not self._is_running:
                return

            self._remaining_seconds -= 1

            self.send_tick_influx()

            if self._remaining_seconds <= 0:
                self._remaining_seconds = 0
                self._is_running = False
                self._update_display()
                self._start_blinking()
                log(f"[{self.name}] Timer finished!")
            else:
                self._update_display()
                self._schedule_tick()

    def _start_blinking(self):
        self._is_blinking = True
        log(f"[{self.name}] Starting blink mode")
        self._blink_cycle()

    def _blink_cycle(self):
        if not self._is_blinking:
            return

        if hasattr(self, '_blink_state'):
            self._blink_state = not self._blink_state
        else:
            self._blink_state = True

        if self._blink_state:
            self.output.display_time(0, 0)
        else:
            self.output.clear()

        self._blink_thread = threading.Timer(0.5, self._blink_cycle)
        self._blink_thread.start()

    def _stop_blinking(self):
        self._is_blinking = False
        if self._blink_thread:
            self._blink_thread.cancel()
            self._blink_thread = None

    def _update_display(self):
        if self._is_blinking:
            return

        minutes = self._remaining_seconds // 60
        seconds = self._remaining_seconds % 60
        self.output.display_time(minutes, seconds)

    def _format_time(self, total_seconds):
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def get_remaining_time(self):
        return {
            "remaining_seconds": self._remaining_seconds,
            "formatted": self._format_time(self._remaining_seconds),
            "is_running": self._is_running,
            "is_blinking": self._is_blinking
        }

    def set_add_seconds(self, seconds: int):
        with self._lock:
            self.add_seconds = seconds
            log(f"[{self.name}] Button press now adds {seconds}s")

    def send_tick_influx(self):
        self.mqtt_client.send(
            MqttTelegrafSingleFieldPoint(
                "FOUR_SD",
                self.device_name,
                self.name,
                self._remaining_seconds,
                self.output.is_simulated()
            )
        )