import threading
import time

from RPi import GPIO

from shared.actuators.buzzer.component import initialize_buzzer
from shared.actuators.door_light.component import initialize_door_light
from shared.alarm.alarm_system import AlarmSystem
from shared.config import load_config
from shared.logger.logger import log, logger_loop
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.sensors.door_motion_sensor.component import run_motion_sensor
from shared.sensors.door_sensor.component import run_door_sensor
from shared.sensors.door_ultra_sonic.component import run_ultrasonic_sensor
from shared.sensors.keypad.component import run_keypad

DEVICE_NAME = "PI1"
if __name__ == '__main__':
    config = load_config("PI1/config.json")

    print(config)
    threads = []
    stop_event = threading.Event()

    telgraf_client = MqttTelegrafBatchClient()

    door_buzzer = initialize_buzzer(config["DB"],"DB", DEVICE_NAME, telgraf_client)
    door_light = initialize_door_light(config["DL"],"DL", DEVICE_NAME, telgraf_client)

    alarm = AlarmSystem( "PI1_ALARM", DEVICE_NAME, telgraf_client, subscribers = [door_buzzer])
    GPIO.setmode(GPIO.BCM)
    try:

        run_door_sensor(config['DS1'], threads, stop_event, telgraf_client, "DS1", DEVICE_NAME)
        dus = run_ultrasonic_sensor(config['DUS1'], threads, stop_event, telgraf_client, "DUS1", DEVICE_NAME)
        run_motion_sensor(config['DPIR1'], threads, stop_event, telgraf_client, "DPIR1", DEVICE_NAME, [dus, door_light])
        run_keypad(config['DMS'], threads, stop_event, telgraf_client, "DMS", DEVICE_NAME)

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
    finally:
        GPIO.cleanup()
