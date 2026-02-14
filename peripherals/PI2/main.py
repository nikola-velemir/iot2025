import threading
import time

from shared.actuators.buzzer.actuator import DoorBuzzerActuator
from shared.actuators.buzzer.output import SimulatedBuzzer
from shared.actuators.stopwatch.actuator import KitchenStopwatch
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

if __name__ == '__main__':
    config = load_config("PI2/config.json")
    print(config)
    threads = []
    stop_event = threading.Event()
    telegraf_client = MqttTelegrafBatchClient()

    door_buzzer = DoorBuzzerActuator(SimulatedBuzzer(), "DBZ2", "PI2", telegraf_client)

    kitchen_stopwatch = KitchenStopwatch(SimulatedStopwatchOutput(), "4SD", "PI2", telegraf_client)
    alarm = AlarmSystem( "PI1_ALARM", "PI1", telegraf_client, subscribers = [door_buzzer])

    try:
        run_gyro_sensor(config["GYR"], threads, stop_event, telegraf_client, "GYR", "PI2")
        dus = run_ultrasonic_sensor(config["DUS2"], threads, stop_event, telegraf_client, "DUS2", "PI2")
        run_dht_sensor(config["DHT3"], threads,stop_event, telegraf_client,"DHT3","PI2")
        run_door_sensor(config["DS2"], threads, stop_event, telegraf_client,"DS2","PI2")
        run_motion_sensor(config['DPIR2'], threads, stop_event, telegraf_client, "DPIR2", "PI2", [dus])
        run_button(config['BTN'], threads, stop_event, telegraf_client, "BTN", 'Kitchen Button', "PI2", [kitchen_stopwatch])
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

