import threading
import time

from shared.logger.logger import log
from shared.actuators.door_light.input import SimulatedLightInput
from shared.actuators.door_light.actuator import DoorLightSensor
from shared.sensors.door_sensor.input import SimulatedButton
from shared.sensors.door_sensor.sensor import DoorSensor
from shared.sensors.door_sensor.simulator import run_door_sensor_simulator

def run_door_sensor_polling(sensor: DoorSensor, stop_event, interval=0.1):
    while not stop_event.is_set():
        sensor.poll()
        time.sleep(interval)


def run_door_sensor(config, threads, stop_event):
    if not config['simulated']:
        return

    log("Starting DS1 simulator")

    door_sensor = DoorSensor(SimulatedButton())

    simulator_thread = threading.Thread(
        name="DS1-simulator",
        target=run_door_sensor_simulator,
        args=(2, door_sensor, stop_event),
        daemon=True
    )

    poller_thread = threading.Thread(
        name="DS1-poller",
        target=run_door_sensor_polling,
        args=(door_sensor, stop_event),
        daemon=True
    )

    simulator_thread.start()
    poller_thread.start()

    threads.extend([simulator_thread, poller_thread])

    log("DS1 simulator started")
