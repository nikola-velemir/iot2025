import threading
from shared.logger.logger import log
from shared.sensors.keypad.sensor import KeyPad
from shared.sensors.keypad.input import SimulatedKeypad
from shared.sensors.keypad.simulator import simulated_keypad_input_loop

VALID_KEYS = "0123456789ABCD*#"

def run_keypad_polling(sensor, stop_event, interval=0.1):
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)

def run_keypad(config, threads, stop_event):
    if not config.get("simulated", False):
        return

    log("Starting KEYPAD simulator")

    poll_interval = config.get("poll_interval", 0.1)

    keypad_input = SimulatedKeypad()
    keypad_sensor = KeyPad(keypad_input)

    simulator_thread = threading.Thread(
        name="KEYPAD-simulator",
        target=simulated_keypad_input_loop,
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
