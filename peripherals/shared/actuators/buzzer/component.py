from shared.actuators.buzzer.actuator import DoorBuzzerActuator
from shared.actuators.buzzer.output import SimulatedBuzzer, GpioBuzzer


def initialize_buzzer(config, actuator_name, device_name, telgraf_client):
    actuator_output = SimulatedBuzzer()
    if not config["simulated"]:
        actuator_output = GpioBuzzer(-1)  # menjace se radi gpio koda

    door_buzzer = DoorBuzzerActuator(actuator_output, actuator_name, device_name, telgraf_client)
    return door_buzzer
