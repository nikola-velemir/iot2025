from shared.actuators.door_light.actuator import DoorLightActuator
from shared.actuators.door_light.output import SimulatedLightOutput, GpioLightOutput


def initialize_door_light(config, actuator_name, device_name, telgraf_client):
    actuator_output = SimulatedLightOutput()
    if not config["simulated"]:
        actuator_output = GpioLightOutput(-1) #menjace se radi gpio koda
    door_light = DoorLightActuator(
        actuator_output,
        actuator_name,
        device_name,
        telgraf_client)
    return door_light
