import threading
from shared.logger.logger import log
from shared.actuators.door_light.input import SimulatedLightInput
from shared.actuators.door_light.actuator import DoorLightSensor
from shared.actuators.door_light.simulator import run_door_light_sensor_simulator


def run_door_light_sensor_polling(sensor, stop_event, interval=0.1):
    """Poll the sensor state in the background."""
    while not stop_event.is_set():
        sensor.poll()
        stop_event.wait(interval)


def run_door_light_sensor(config, threads, stop_event):
    """Start the door light sensor simulator with command input."""
    if not config.get("simulated", False):
        return

    log("Starting LS1 simulator")

    poll_interval = config.get("poll_interval", 0.1)
    light_sensor = DoorLightSensor(SimulatedLightInput())

    # Start poller thread (daemon)
    poller_thread = threading.Thread(
        name="LS1-poller",
        target=run_door_light_sensor_polling,
        args=(light_sensor, stop_event, poll_interval),
        daemon=True,
    )
    poller_thread.start()
    threads.append(poller_thread)

    log("LS1 command input ready. Type 'led on', 'led off', or 'q' to quit.")

    # Run command input loop in the main thread (blocking)
    run_door_light_sensor_simulator(light_sensor, stop_event)

    stop_event.set()
    log("LS1 simulator stopped")
