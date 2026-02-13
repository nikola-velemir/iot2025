import threading
import time

from shared.logger.logger import log
from shared.sensors.gyroscope.input import GpioGyroscope, SimulatedGyroscope
from shared.sensors.gyroscope.sensor import GyroscopeSensor
from shared.sensors.gyroscope.simulator import run_gyro_simulator


def run_gyro_sensor(config, threads, stop_event, mqtt_client, sensor_name, device_name):
    if not config['simulated']:
        log(f"Starting hardware Gyroscope: {sensor_name}")
        gyro_input = GpioGyroscope()
    else:
        log(f"Starting simulated Gyroscope: {sensor_name}")
        gyro_input = SimulatedGyroscope()

        gyro_sensor = GyroscopeSensor(gyro_input, sensor_name, device_name, mqtt_client)

        sim_thread = threading.Thread(
            target=run_gyro_simulator,
            args=(gyro_sensor, stop_event),
            daemon=True
        )
        sim_thread.start()
        threads.append(sim_thread)

    gyro_sensor = GyroscopeSensor(gyro_input, sensor_name, device_name, mqtt_client)

    def poller():
        while not stop_event.is_set():
            gyro_sensor.poll()
            time.sleep(config.get('interval', 2.0))

    poller_thread = threading.Thread(target=poller, daemon=True)
    poller_thread.start()
    threads.append(poller_thread)

    log(f"Gyroscope {sensor_name} started")