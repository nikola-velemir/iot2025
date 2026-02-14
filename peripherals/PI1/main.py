import threading
import time

from shared.alarm.alarm_system import AlarmSystem
from shared.actuators.buzzer.actuator import DoorBuzzerActuator
from shared.actuators.buzzer.output import SimulatedBuzzer
from shared.actuators.door_light.actuator import DoorLightActuator
from shared.actuators.door_light.output import SimulatedLightOutput
from shared.config import load_config
from shared.logger.logger import log, logger_loop
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.sensors.door_motion_sensor.component import run_motion_sensor
from shared.sensors.door_sensor.component import run_door_sensor
from shared.sensors.door_ultra_sonic.component import run_ultrasonic_sensor
from shared.sensors.keypad.component import run_keypad

if __name__ == '__main__':
    config = load_config("PI1/config.json")
    print(config)
    threads = []
    stop_event = threading.Event()

    telgraf_client = MqttTelegrafBatchClient()

    door_buzzer = DoorBuzzerActuator(SimulatedBuzzer(), "DB", "PI1", telgraf_client) # todo proslediti config
    door_light = DoorLightActuator(SimulatedLightOutput(), "DL", "PI1", telgraf_client) # todo proslediti config

    alarm = AlarmSystem( "PI1_ALARM", "PI1", telgraf_client, subscribers = [door_buzzer])

    try:
        run_door_sensor(config['DS1'], threads, stop_event, telgraf_client, "DS1", "PI1")
        dus = run_ultrasonic_sensor(config['DUS1'], threads, stop_event, telgraf_client, "DUS1", "PI1")
        run_motion_sensor(config['DPIR1'], threads, stop_event, telgraf_client, "DPIR1", "PI1", [dus, door_light])
        run_keypad(config['DMS'], threads, stop_event, telgraf_client, "DMS", "PI1")

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

