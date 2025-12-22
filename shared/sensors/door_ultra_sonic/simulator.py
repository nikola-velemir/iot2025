import random

from sensors.door_ultra_sonic.sensor import UltrasonicSensor


def run_ultrasonic_sensor_simulator(delay, us_sensor: UltrasonicSensor, stop_event):
    """
    Simulates an ultrasonic sensor by changing its distance every `delay` seconds.
    """
    while not stop_event.is_set():
        us_sensor.input_device.read_distance()  # we need a setter in the input

        if stop_event.wait(delay):
            break