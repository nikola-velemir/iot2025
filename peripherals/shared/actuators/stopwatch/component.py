from shared.actuators.stopwatch.actuator import KitchenStopwatch
from shared.actuators.stopwatch.output import SimulatedStopwatchOutput, GpioStopwatchOutput


def initialize_stopwatch(config, actuator_name, device_name, telegraf_client):
    output = SimulatedStopwatchOutput()
    if not config["simulated"]:
        output = GpioStopwatchOutput(0x10)
    kitchen_stopwatch = KitchenStopwatch(output, actuator_name, device_name, telegraf_client)
    return kitchen_stopwatch