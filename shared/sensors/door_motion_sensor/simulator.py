from shared.sensors.door_motion_sensor.input import SimulatedMotionInput
from shared.sensors.door_motion_sensor.sensor import DoorMotionSensor


def run_motion_sensor_simulator(sensor: DoorMotionSensor, stop_event, interval=2):
    """
    Simulates motion sensor by randomly toggling motion every `interval` seconds
    """
    while not stop_event.is_set():
        # simulate new motion state
        if isinstance(sensor.motion_input, SimulatedMotionInput):
            sensor.motion_input.simulate_motion()
        if stop_event.wait(interval):
            break
