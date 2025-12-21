import threading
import time

from actuators.keypad.actuator import KeyPad
from actuators.keypad.input import SimulatedKeypad
from actuators.keypad.simulator import run_keypad_simulator
from logger.logger import log


def run_keypad_polling(sensor, stop_event, interval=0.05):
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)


def run_keypad(config, threads, stop_event):
    if not config.get("simulated", False):
        # Later: GPIO keypad implementation
        return

    log("Starting KEYPAD simulator")

    poll_interval = config.get("poll_interval", 0.05)

    keypad_input = SimulatedKeypad()
    keypad_sensor = KeyPad(keypad_input)

    simulator_thread = threading.Thread(
        name="KEYPAD-simulator",
        target=run_keypad_simulator,
        args=(keypad_input, stop_event),
        daemon=True
    )

    poller_thread = threading.Thread(
        name="KEYPAD-poller",
        target=run_keypad_polling,
        args=(keypad_sensor, stop_event, poll_interval),
        daemon=True
    )

    simulator_thread.start()
    poller_thread.start()

    threads.extend([simulator_thread, poller_thread])

    log("KEYPAD simulator started")