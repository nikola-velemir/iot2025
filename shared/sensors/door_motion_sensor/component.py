from shared.sensors.door_motion_sensor.input import SimulatedMotionInput, GpioMotionInput
from shared.sensors.door_motion_sensor.sensor import DoorMotionSensor
from shared.logger.logger import log
import threading

def run_motion_sensor_polling(sensor: DoorMotionSensor, stop_event, interval=0.1):
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)

def run_motion_sensor(config, threads, stop_event, mqtt_client, sensor_name, device_name, subscribers = None):
    if subscribers is None:
        subscribers = []

    if not config['simulated']:
        log("Starting DPIR1 sensor")
        motion_sensor = DoorMotionSensor(GpioMotionInput(config['pin']), sensor_name, device_name, mqtt_client)
    else:
        log("Starting DPIR1 simulator")
        motion_sensor = DoorMotionSensor(SimulatedMotionInput(), sensor_name, device_name, mqtt_client)

    for sub in subscribers:
        motion_sensor.subscribe(sub)

    poll_interval = config.get('poll_interval', 1.0)

    poller_thread = threading.Thread(
        name="Motion-poller",
        target=run_motion_sensor_polling,
        args=(motion_sensor, stop_event, poll_interval),
        daemon=True
    )

    poller_thread.start()
    threads.extend([poller_thread])

    log("Motion sensor simulator started")