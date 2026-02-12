from shared.sensors.door_sensor.input import SimulatedButton
from shared.sensors.door_sensor.sensor import DoorSensor


def run_door_sensor_simulator(delay, door_sensor: DoorSensor, stop_event):
    button: SimulatedButton = door_sensor.button

    while not stop_event.is_set():
        button.press()
        if stop_event.wait(delay):
            break

        button.release()
        if stop_event.wait(delay):
            break
