import threading

from shared.logger.logger import log
from shared.sensors.door_ultra_sonic.input import SimulatedUltrasonicInput
from shared.sensors.door_ultra_sonic.sensor import UltrasonicSensor


def run_ultrasonic_sensor_polling(sensor: UltrasonicSensor, stop_event, interval=0.5):
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)


def run_ultrasonic_sensor(config, threads, stop_event):
    if not config.get('simulated', False):
        return

    log("Starting Ultrasonic simulator")

    interval = config.get('poll_interval', 0.5)
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
