import threading
import time

from sensors.door_light.input import SimulatedLightInput
from sensors.door_light.sensor import DoorLightSensor
from sensors.door_sensor.input import SimulatedButton
from sensors.door_sensor.sensor import DoorSensor
from sensors.door_sensor.simulator import run_door_sensor_simulator

def run_door_sensor_polling(sensor: DoorSensor, stop_event, interval=0.1):
    while not stop_event.is_set():
        sensor.poll()
        time.sleep(interval)


def run_door_sensor(config, threads, stop_event):
    if not config['simulated']:
        return

    print("Starting DS1 simulator")

    door_sensor = DoorSensor(SimulatedButton())
    light_sensor = DoorLightSensor(SimulatedLightInput())

    # 🔗 subscription
    door_sensor.subscribe(light_sensor.handle_door_event)

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

    print("DS1 simulator started")
