import threading

from logger.logger import log
from sensors.door_light.input import SimulatedLightInput
from sensors.door_light.sensor import DoorLightSensor
from sensors.door_light.simulator import run_door_light_sensor_simulator


def run_door_light_sensor_polling(sensor, stop_event, interval=0.1):
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)


def run_door_light_sensor(config, threads, stop_event):
    if not config.get('simulated', False):
        return

    log("Starting LS1 simulator")

    delay = config.get('toggle_interval', 2)
    poll_interval = config.get('poll_interval', 0.1)

    light_sensor = DoorLightSensor(SimulatedLightInput())

    simulator_thread = threading.Thread(
        name="LS1-simulator",
        target=run_door_light_sensor_simulator,
        args=(delay, light_sensor, stop_event),
        daemon=True
    )

    poller_thread = threading.Thread(
        name="LS1-poller",
        target=run_door_light_sensor_polling,
        args=(light_sensor, stop_event, poll_interval),
        daemon=True
    )

    simulator_thread.start()
    poller_thread.start()

    threads.extend([simulator_thread, poller_thread])

    log("LS1 simulator started")
