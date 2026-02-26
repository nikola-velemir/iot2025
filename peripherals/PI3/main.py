import threading
import time

from RPi import GPIO

from shared.actuators.brgb.component import initialize_brgb
from shared.actuators.lcd.component import initialize_lcd
from shared.config import load_config
from shared.logger.logger import log, logger_loop
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.sensors.dht_sensor.component import run_dht_sensor
from shared.sensors.door_motion_sensor.component import run_motion_sensor
from shared.sensors.infra_red_sensor.component import run_ir_sensor

DEVICE_NAME = "PI3"
if __name__ == "__main__":
    config = load_config("PI3/config.json")
    print(config)
    threads = []
    stop_event = threading.Event()
    telegraf_client = MqttTelegrafBatchClient()

    brgb = initialize_brgb(config["BRGB"],"BRGB", DEVICE_NAME, telegraf_client)
    lcd = initialize_lcd(config["LCD"],"LCD", DEVICE_NAME, telegraf_client)

    try:
        #run_dht_sensor(config["DHT2"], threads,stop_event, telegraf_client,"DHT2",DEVICE_NAME, subscribers=[lcd])
        #run_dht_sensor(config["DHT1"], threads,stop_event, telegraf_client,"DHT1",DEVICE_NAME, subscribers=[lcd])
        run_ir_sensor(config["IR"], threads, stop_event, telegraf_client, "IR", DEVICE_NAME, subscribers=[brgb])
        #run_motion_sensor(config["DPIR3"], threads, stop_event, telegraf_client, "DPIR3", DEVICE_NAME)
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