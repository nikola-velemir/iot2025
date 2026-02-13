import threading
import time

from shared.logger.logger import log
from shared.sensors.button.sensor import Button
from shared.sensors.door_sensor.input import SimulatedButton, GpioButton
from shared.sensors.door_sensor.sensor import DoorSensor
from shared.sensors.door_sensor.simulator import run_door_sensor_simulator

def run_button_sensor_polling(sensor: DoorSensor, stop_event, interval=10.0):
    while not stop_event.is_set():
        sensor.poll()
        time.sleep(interval)

def run_button(config, threads, stop_event, mqtt_client, sensor_name,full_name, device_name, subscribers = None):
    simulator_thread = None
    if subscribers is None:
        subscribers = []

    if not config['simulated']:
        log(f"Starting {sensor_name} sensor")
        door_sensor = Button(GpioButton(config['pin']),full_name, sensor_name, device_name, mqtt_client)
    else:
        log(f"Starting {sensor_name} simulator")
        door_sensor = Button(SimulatedButton(),full_name,  sensor_name, device_name, mqtt_client)

        simulator_thread = threading.Thread(
            name=f"{full_name}",
            target=run_door_sensor_simulator,
            args=(2, door_sensor, stop_event),
            daemon=True
        )

    door_sensor.subscribe_multiple(subscribers)

    poller_thread = threading.Thread(
        name=f"{sensor_name}-poller",
        target=run_button_sensor_polling,
        args=(door_sensor, stop_event),
        daemon=True
    )

    if simulator_thread:
        simulator_thread.start()
        threads.extend([simulator_thread])

    poller_thread.start()
    threads.extend([poller_thread])

    log(f"{full_name} button started")
