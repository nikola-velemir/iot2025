import time
import random
from shared.sensors.infra_red_sensor.input import SimulatedIR


def run_ir_simulator(ir_sensor, stop_event):

    ir_input: SimulatedIR = ir_sensor.ir_input

    commands = [
        "ON", "OFF",
        "RED", "GREEN", "BLUE", "WHITE",
        "BRIGHT_UP", "BRIGHT_DOWN",
        "FLASH", "STROBE", "FADE", "SMOOTH"
    ]

    while not stop_event.is_set():
        time.sleep(random.uniform(5.0, 15.0))

        command = random.choice(commands)


        if hasattr(ir_input, 'simulate_press'):
            ir_input.simulate_press(command)

        if stop_event.is_set():
            break