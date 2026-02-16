from shared.actuators.buzzer.actuator import DoorBuzzerActuator
from shared.actuators.buzzer.output import SimulatedBuzzer, GpioBuzzer


def initialize_buzzer(config, actuator_name, device_name, telgraf_client):
    actuator_output = SimulatedBuzzer()
    if not config["simulated"]:
        pin = config["pins"]["buzzer_pin"]
        duty_cycle = config["duty_cycle"]
        frequency = config["frequency"]
        actuator_output = GpioBuzzer(pin, duty_cycle, frequency)  # menjace se radi gpio koda

    door_buzzer = DoorBuzzerActuator(actuator_output, actuator_name, device_name, telgraf_client)
    return door_buzzer
