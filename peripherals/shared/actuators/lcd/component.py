from shared.actuators.lcd.actuator import LcdActuator
from shared.actuators.lcd.output import SimulatedLcd, GpioLcd


def initialize_lcd(config, actutor_name, device_name, telegraf_client):
    actuator_output = SimulatedLcd()
    if not config["simulated"]:
        actuator_output = GpioLcd(
            config["address"]
        )

    lcd = LcdActuator(actuator_output, actutor_name, device_name, telegraf_client)
    return lcd