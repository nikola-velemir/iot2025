import threading
import time

from RPi import GPIO

from shared.actuators.stopwatch.actuator import KitchenStopwatch
from shared.actuators.stopwatch.component import initialize_stopwatch
from shared.actuators.stopwatch.output import SimulatedStopwatchOutput
from shared.alarm.alarm_system import AlarmSystem
from shared.config import load_config
from shared.logger.logger import logger_loop, log
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.sensors.button.component import run_button
from shared.sensors.dht_sensor.component import run_dht_sensor
from shared.sensors.door_motion_sensor.component import run_motion_sensor
from shared.sensors.door_sensor.component import run_door_sensor
from shared.sensors.door_ultra_sonic.component import run_ultrasonic_sensor
from shared.sensors.gyroscope.component import run_gyro_sensor

DEVICE_NAME = "PI2"

if __name__ == '__main__':
    config = load_config("PI2/config.json")
    print(config)
    threads = []
    stop_event = threading.Event()
    telegraf_client = MqttTelegrafBatchClient()
    GPIO.setmode(GPIO.BCM)

    kitchen_stopwatch = initialize_stopwatch(config["FOUR_SD"], "FOUR_SD", DEVICE_NAME, telegraf_client)
    alarm = AlarmSystem( "PI1_ALARM", DEVICE_NAME, telegraf_client, subscribers=[])
    try:
        run_gyro_sensor(config["GYR"], threads, stop_event, telegraf_client, "GYR", DEVICE_NAME)
        dus = run_ultrasonic_sensor(config["DUS2"], threads, stop_event, telegraf_client, "DUS2", DEVICE_NAME)
        run_dht_sensor(config["DHT3"], threads,stop_event, telegraf_client,"DHT3",DEVICE_NAME)
        run_door_sensor(config["DS2"], threads, stop_event, telegraf_client,"DS2",DEVICE_NAME)
        run_motion_sensor(config['DPIR2'], threads, stop_event, telegraf_client, "DPIR2", DEVICE_NAME, [dus])
        run_button(config['BTN'], threads, stop_event, telegraf_client, "BTN", 'Kitchen Button', DEVICE_NAME, [kitchen_stopwatch])
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