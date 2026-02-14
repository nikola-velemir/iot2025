import threading
import time

from shared.actuators.brgb.brgb import BRGB
from shared.actuators.lcd.actuator import LcdActuator
from shared.actuators.lcd.output import SimulatedLcd
from shared.config import load_config
from shared.logger.logger import log, logger_loop
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient
from shared.sensors.dht_sensor.component import run_dht_sensor
from shared.sensors.door_motion_sensor.component import run_motion_sensor
from shared.sensors.infra_red_sensor.component import run_ir_sensor

if __name__ == "__main__":
    config = load_config("PI3/config.json")
    print(config)
    threads = []
    stop_event = threading.Event()
    telegraf_client = MqttTelegrafBatchClient()

    brgb = BRGB(config["BRGB"],'PI2', telegraf_client)
    #lcd = LcdActuator(SimulatedLcd(), config["LCD"], "PI3")



    try:
        # run_dht_sensor(config["DHT2"], threads,stop_event, mqtt_client,"DHT2","PI3", subscribers=[lcd])
        # run_dht_sensor(config["DHT1"], threads,stop_event, mqtt_client,"DHT1","PI3", subscribers=[lcd])
        run_ir_sensor(config["IR"], threads, stop_event, telegraf_client, "IR", "PI3", subscribers=[brgb])
        # run_motion_sensor(config["DPIR3"], threads, stop_event, mqtt_client, "DPIR3", "PI3")
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