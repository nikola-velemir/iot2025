import threading
import time

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
    mqtt_client = MqttTelegrafBatchClient()
    try:
        run_gyro_sensor(config["GSG"], threads, stop_event, mqtt_client, "GSG", "PI2")
        dus = run_ultrasonic_sensor(config["DUS2"], threads, stop_event, mqtt_client, "DUS2", "PI2")
        run_dht_sensor(config["DHT3"], threads,stop_event, mqtt_client,"DHT3","PI2")
        run_door_sensor(config["DS2"], threads, stop_event, mqtt_client,"DS2","PI2")
        run_motion_sensor(config['DPIR2'], threads, stop_event, mqtt_client, "DPIR2", "PI2", [dus])
        run_button(config['BTN'], threads, stop_event, mqtt_client, "BTN", 'Kitchen Button',"PI2", [dus])
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

