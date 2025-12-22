from shared.actuators.buzzer.actuator import DoorBuzzer
from shared.actuators.buzzer.output import SimulatedBuzzer
from shared.sensors.door_motion_sensor.input import SimulatedMotionInput
from shared.sensors.door_motion_sensor.sensor import DoorMotionSensor
from shared.sensors.door_motion_sensor.simulator import run_motion_sensor_simulator
from shared.logger.logger import log


def run_motion_sensor_polling(sensor: DoorMotionSensor, stop_event, interval=0.1):
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)

import threading

def run_motion_sensor(config, threads, stop_event):
    if not config.get('simulated', False):
        return

    log("Starting Motion sensor simulator")

    interval = config.get('motion_toggle_interval', 2)
    poll_interval = config.get('poll_interval', 0.1)

    motion_sensor = DoorMotionSensor(SimulatedMotionInput())

    buzzer = DoorBuzzer(SimulatedBuzzer())

    motion_sensor.subscribe(buzzer.handle_motion_event)
    simulator_thread = threading.Thread(
        name="Motion-simulator",
        target=run_motion_sensor_simulator,
        args=(motion_sensor, stop_event, interval),
        daemon=True
    )

    poller_thread = threading.Thread(
        name="Motion-poller",
        target=run_motion_sensor_polling,
        args=(motion_sensor, stop_event, poll_interval),
        daemon=True
    )

    simulator_thread.start()
    poller_thread.start()

    threads.extend([simulator_thread, poller_thread])

    log("Motion sensor simulator started")