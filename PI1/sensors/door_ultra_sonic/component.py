from logger.logger import log
from sensors.door_ultra_sonic.input import SimulatedUltrasonicInput
from sensors.door_ultra_sonic.sensor import UltrasonicSensor
import threading

from sensors.door_ultra_sonic.simulator import run_ultrasonic_sensor_simulator


def run_ultrasonic_sensor_polling(sensor: UltrasonicSensor, stop_event, interval=0.2):
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)


def run_ultrasonic_sensor(config, threads, stop_event):
    if not config.get('simulated', False):
        return

    log("Starting Ultrasonic simulator")

    interval = config.get('poll_interval', 0.2)
    sensor = UltrasonicSensor(SimulatedUltrasonicInput())

    poller_thread = threading.Thread(
        name="US1-poller",
        target=run_ultrasonic_sensor_polling,
        args=( sensor, stop_event,interval),
        daemon=True
    )

    poller_thread.start()
    threads.append(poller_thread)

    log("Ultrasonic simulator started")
