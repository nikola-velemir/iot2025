import math
import time

from shared.sensors.gyroscope.input import SimulatedGyroscope


def run_gyro_simulator(gyro_sensor, stop_event):
    gyro_input: SimulatedGyroscope = gyro_sensor.gyro_input
    counter = 0

    while not stop_event.is_set():
        # Simulate a slight wobble using sine waves
        x = math.sin(counter) * 0.5
        y = math.cos(counter) * 0.3
        z = math.sin(counter / 2) * 0.1

        gyro_input.set_data(round(x, 3), round(y, 3), round(z, 3))

        counter += 0.5
        if stop_event.wait(1):  # Update every second
            break