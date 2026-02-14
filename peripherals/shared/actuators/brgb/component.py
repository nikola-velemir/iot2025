from shared.actuators.brgb.actuator import BRGB
from shared.actuators.brgb.output import SimulatedBRGBOutput, GpioBRGBOutput


def initialize_brgb(config, actuator_name, device_name, telegraf_client):
    output = SimulatedBRGBOutput(actuator_name)
    if not config["simulated"]:
        output = GpioBRGBOutput(actuator_name, -1, -2, -3)
    brgb = BRGB(output, actuator_name, device_name, telegraf_client)
    return brgb
