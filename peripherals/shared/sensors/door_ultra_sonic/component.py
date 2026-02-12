import threading

from shared.logger.logger import log
from shared.sensors.door_ultra_sonic.input import SimulatedUltrasonicInput, GpioUltrasonicInput
from shared.sensors.door_ultra_sonic.sensor import UltrasonicSensor

def run_ultrasonic_sensor_polling(sensor: UltrasonicSensor, stop_event, interval=0.5):
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)

def run_ultrasonic_sensor(config, threads, stop_event, mqtt_client, sensor_name, device_name):
    if not config['simulated']:
        log("Starting DUS1 sensor")
        ultrasonic_sensor = UltrasonicSensor(GpioUltrasonicInput(config['pin']), sensor_name, device_name, mqtt_client)
    else:
        log("Starting DUS1 simulator")
        ultrasonic_sensor = UltrasonicSensor(SimulatedUltrasonicInput(), sensor_name, device_name, mqtt_client)

    interval = config.get('poll_interval', 0.5)

    poller_thread = threading.Thread(
        name="US1-poller",
        target=run_ultrasonic_sensor_polling,
        args=(ultrasonic_sensor, stop_event,interval),
        daemon=True
    )

    poller_thread.start()
    threads.append(poller_thread)

    log("US1 started")
