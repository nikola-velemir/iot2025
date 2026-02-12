import threading
import time

from shared.config import load_config
from shared.logger.logger import logger_loop, log
from shared.mqtt.influx.mqtt_telegraf import MqttTelegrafBatchClient

if __name__ == '__main__':
    config = load_config("PI2/config.json")
    print(config)
    threads = []
    stop_event = threading.Event()
    mqtt_client = MqttTelegrafBatchClient()
    try:

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

