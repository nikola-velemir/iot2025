import threading
import time

from shared.logger.logger import log
from shared.sensors.door_sensor.input import SimulatedButton, GpioButton
from shared.sensors.door_sensor.sensor import DoorSensor
from shared.sensors.door_sensor.simulator import run_door_sensor_simulator

def run_door_sensor_polling(sensor: DoorSensor, stop_event, interval=1.0):
    while not stop_event.is_set():
        sensor.poll()
        time.sleep(interval)

def run_door_sensor(config, threads, stop_event, mqtt_client, sensor_name, device_name, subscribers = None):
    simulator_thread = None
    if subscribers is None:
        subscribers = []

    if not config['simulated']:
        log("Starting DS1 sensor")
        door_sensor = DoorSensor(GpioButton(config['pin']), sensor_name, device_name, mqtt_client)
    else:
        log("Starting DS1 simulator")
        door_sensor = DoorSensor(SimulatedButton(), sensor_name, device_name, mqtt_client)

        simulator_thread = threading.Thread(
            name="DS1-simulator",
            target=run_door_sensor_simulator,
            args=(2, door_sensor, stop_event),
            daemon=True
        )

    for sub in subscribers:
        door_sensor.subscribe(sub)

    poller_thread = threading.Thread(
        name="DS1-poller",
        target=run_door_sensor_polling,
        args=(door_sensor, stop_event),
        daemon=True
    )

    if simulator_thread:
        simulator_thread.start()
        threads.extend([simulator_thread])

    poller_thread.start()
    threads.extend([poller_thread])

    log("DS1 button started")
