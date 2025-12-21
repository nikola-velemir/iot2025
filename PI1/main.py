import threading
import time

from actuators.keypad.component import run_keypad
from config import load_config
from logger.logger import log, logger_loop
from sensors.door_motion_sensor.component import run_motion_sensor
from sensors.door_sensor.component import run_door_sensor
from sensors.door_ultra_sonic.component import run_ultrasonic_sensor

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

        dpir1_settings = config['DPIR1']
        run_motion_sensor(dpir1_settings, threads, stop_event)
        dms_settings = config['DMS']
        run_keypad(dms_settings, threads,stop_event)
        threading.Thread(
            target=logger_loop,
            args=(stop_event,),
            daemon=True
        ).start()
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        log('Stopping app')
        for t in threads:
            stop_event.set()

