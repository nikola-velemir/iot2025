import threading
import time

from shared.logger.logger import log
from shared.sensors.infra_red_sensor.input import SimulatedIR, GpioIR
from shared.sensors.infra_red_sensor.sensor import IRSensor
# Importujemo simulator koji smo gore definisali
from shared.sensors.infra_red_sensor.simulator import run_ir_simulator


def run_ir_sensor(config, threads, stop_event, mqtt_client, sensor_name, device_name, subscribers=None):
    ir_input = None

    if subscribers is None:
        subscribers = []

    if not config['simulated']:
        log(f"Starting hardware IR Receiver: {sensor_name}")
        ir_input = GpioIR(config['pins']['ir_pin'])
    else:
        log(f"Starting simulated IR Receiver: {sensor_name}")
        ir_input = SimulatedIR()

    ir_sensor = IRSensor(ir_input, sensor_name, device_name, mqtt_client)

    ir_sensor.subscribe_multiple(subscribers)

    if config['simulated']:
        sim_thread = threading.Thread(
            name=f"{sensor_name}-simulator",
            target=run_ir_simulator,
            args=(ir_sensor, stop_event),
            daemon=True
        )
        sim_thread.start()
        threads.append(sim_thread)

    # poll_time = config.get("poll_time",0.05)
    # def poller():
    #     log(f"{sensor_name} poller started.")
    #     while not stop_event.is_set():
    #         ir_sensor.poll()
    #         time.sleep(0.0005)
    #
    # poller_thread = threading.Thread(
    #     name=f"{sensor_name}-poller",
    #     target=poller,
    #     daemon=True
    # )
    # poller_thread.start()
    # threads.append(poller_thread)

    log(f"{sensor_name} started successfully")