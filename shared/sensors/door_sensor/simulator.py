import time


def run_door_sensor_simulator(delay, doorSensor, stop_event):
    button = doorSensor.button

    while not stop_event.is_set():
        button.press()
        if stop_event.wait(delay):
            break

        button.release()
        if stop_event.wait(delay):
            break
