import threading
import time

from shared.actuators.door_light.component import run_door_light_sensor
from shared.actuators.input_loop import run_simulated_inputs
from shared.config import load_config
from shared.logger.logger import log, logger_loop
from shared.sensors.door_motion_sensor.component import run_motion_sensor
from shared.sensors.door_sensor.component import run_door_sensor
from shared.sensors.door_ultra_sonic.component import run_ultrasonic_sensor
from shared.sensors.keypad.component import run_keypad

if __name__ == '__main__':
    config = load_config("PI1/config.json")
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

        dl_setting = config['DL']
        dms_setting = config['DMS']
        buzz_setting = config['DB']
        run_simulated_inputs(dl_setting, dms_setting, buzz_setting, threads, stop_event)
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

