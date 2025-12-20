# This is a sample Python script.
import threading
import time

from config import load_config
from sensors.door_light.component import run_door_light_sensor
from sensors.door_sensor.component import run_door_sensor
from sensors.door_ultra_sonic.component import run_ultrasonic_sensor


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config = load_config()
    print(config)
    threads = []
    stop_event = threading.Event()
    try:
        ds1_settings = config['DS1']
        run_door_sensor(ds1_settings, threads, stop_event)
        dus1_settings = config['DUS1']
        run_ultrasonic_sensor(dus1_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()

