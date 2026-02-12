import threading

from shared.logger.logger import log
from shared.sensors.dht_sensor.input import GpioDHT, SimulatedDHT
from shared.sensors.dht_sensor.sensor import DHTSensor
from shared.sensors.dht_sensor.simulator import run_dht_simulator


def run_dht_sensor(config, threads, stop_event, mqtt_client, sensor_name, device_name):
    if not config['simulated']:
        log(f"Starting {sensor_name} hardware")
        dht_input = GpioDHT(config['pin'])
    else:
        log(f"Starting {sensor_name} simulator")
        dht_input = SimulatedDHT()

        dht_sensor = DHTSensor(dht_input, sensor_name, device_name, mqtt_client)

        sim_thread = threading.Thread(
            target=run_dht_simulator,
            args=(dht_sensor, stop_event),
            daemon=True
        )
        sim_thread.start()
        threads.append(sim_thread)

    dht_sensor = DHTSensor(dht_input, sensor_name, device_name, mqtt_client)

    def poller():
        while not stop_event.is_set():
            dht_sensor.poll()
            time.sleep(config.get('interval', 5.0))

    poller_thread = threading.Thread(target=poller, daemon=True)
    poller_thread.start()
    threads.append(poller_thread)