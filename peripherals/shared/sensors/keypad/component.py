import threading
from shared.logger.logger import log
from shared.sensors.keypad.sensor import KeyPad
from shared.sensors.keypad.input import SimulatedKeypad, GpioKeypad
from shared.sensors.keypad.simulator import simulated_keypad_input_loop

def run_keypad_polling(sensor, stop_event, interval=0.1):
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)

def run_keypad(config, threads, stop_event, mqtt_client, sensor_name, device_name, subscribers = None):
    simulator_thread = None
    if subscribers is None:
        subscribers = []

    if not config['simulated']:
        log("Starting DMS1 sensor")
        keypad_sensor = KeyPad(GpioKeypad(config['pins']), sensor_name, device_name, mqtt_client)
    else:
        log("Starting DMS1 simulator")
        keypad_sensor = KeyPad(SimulatedKeypad(), sensor_name, device_name, mqtt_client)

        simulator_thread = threading.Thread(
            name="KEYPAD-simulator",
            target=simulated_keypad_input_loop,
            args=(keypad_sensor, stop_event),
            daemon=True
        )

    for sub in subscribers:
        keypad_sensor.subscribe(sub)

    poll_interval = config.get("poll_interval", 0.1)

    poller_thread = threading.Thread(
        name="KEYPAD-poller",
        target=run_keypad_polling,
        args=(keypad_sensor, stop_event, poll_interval),
        daemon=True
    )

    if simulator_thread:
        simulator_thread.start()
        threads.extend([simulator_thread])

    poller_thread.start()
    threads.extend([poller_thread])

    log("KEYPAD started")
