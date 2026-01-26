import threading
import time

from shared.actuators.buzzer.actuator import DoorBuzzerActuator
from shared.actuators.buzzer.output import SimulatedBuzzer
from shared.actuators.door_light.actuator import DoorLightActuator
from shared.actuators.door_light.output import SimulatedLightOutput
from shared.config import load_config
from shared.logger.logger import log, logger_loop
from shared.mqtt.mqtt_send import MqttBatchClient
from shared.sensors.door_motion_sensor.component import run_motion_sensor
from shared.sensors.door_sensor.component import run_door_sensor
from shared.sensors.door_ultra_sonic.component import run_ultrasonic_sensor
from shared.sensors.keypad.component import run_keypad

if __name__ == '__main__':
    config = load_config("PI1/config.json")
    print(config)
    threads = []
    stop_event = threading.Event()
    mqtt_client = MqttBatchClient()

    door_buzzer = DoorBuzzerActuator(SimulatedBuzzer(), "DBZ1", "PI1", mqtt_client)
    door_light = DoorLightActuator(SimulatedLightOutput(), "DL1", "PI1", mqtt_client)

    try:
        run_door_sensor(config['DS1'], threads, stop_event, mqtt_client, "DS1", "PI1", [door_buzzer, door_light])
        run_ultrasonic_sensor(config['DUS1'], threads, stop_event, mqtt_client, "DUS1", "PI1")
        run_motion_sensor(config['DPIR1'], threads, stop_event, mqtt_client, "DPIR1", "PI1", [door_buzzer])
        run_keypad(config['DMS1'], threads,stop_event, mqtt_client, "DMS1", "PI1")

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

