import random

from shared.sensors.dht_sensor.input import SimulatedDHT


def run_dht_simulator(dht_sensor, stop_event):
    dht_input: SimulatedDHT = dht_sensor.dht_input
    temp = 25.0
    hum = 50.0

    while not stop_event.is_set():
        # Random walk for simulation
        temp += random.uniform(-0.5, 0.5)
        hum += random.uniform(-1.0, 1.0)

        dht_input.set_data(round(temp, 2), round(hum, 2))

        if stop_event.wait(2):  # Update simulation data every 2s
            break