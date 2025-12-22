import threading

from shared.actuators.buzzer.actuator import DoorBuzzer
from shared.actuators.buzzer.output import SimulatedBuzzer
from shared.actuators.door_light.actuator import DoorLightSensor
from shared.actuators.door_light.input import SimulatedLightInput
from shared.sensors.keypad.input import SimulatedKeypad, KeypadInput
from shared.sensors.keypad.sensor import KeyPad
from shared.logger.logger import log

VALID_KEYS = "0123456789ABCD*#"


def simulated_input_loop(keypad: KeyPad, light_sensor: DoorLightSensor, buzzer: DoorBuzzer, stop_event):
    log("Input ready: keys 0-9 A-D * # or commands 'led on', 'led off'. Type Q to quit.")
    while not stop_event.is_set():
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            stop_event.set()
            break

        if not line:
            continue

        if line.upper() == "Q":
            stop_event.set()
            break

        if len(line) == 1 and line.upper() in VALID_KEYS:
            keypad.press_key(line.upper())
            log(f"[KEYPAD] Key pressed: {line.upper()}")
            continue

        line_lower = line.lower()
        if line_lower == "led on":
            light_sensor.light.turn_on()
            log("[CMD DL] LED turned ON")
        elif line_lower == "led off":
            light_sensor.light.turn_off()
            log("[CMD DL] LED turned OFF")
        elif line_lower == "buzzer on":
            buzzer.buzzer.on()
            log("[CMD DB] BUZZER turned ON")
        elif line_lower == "buzzer off":
            buzzer.buzzer.off()
            log("[CMD DB] BUZZER turned OFF")
        else:
            log(f"[INPUT] Unknown input: '{line}'")


def run_simulated_inputs(dl_settings, dms_settings, buzz_settings, threads, stop_event):
    if not dl_settings.get('simulated', False) or not dms_settings.get('simulated', False) or not buzz_settings.get(
            'simulated', False):
        return
    keypad_sensor = KeyPad(SimulatedKeypad())
    light_sensor = DoorLightSensor(SimulatedLightInput())
    buzzer = DoorBuzzer(SimulatedBuzzer())

    # Start the input thread; it runs independently
    simulator_thread = threading.Thread(
        name="Input-simulator",
        target=simulated_input_loop,
        args=(keypad_sensor, light_sensor, buzzer, stop_event),
        daemon=True
    )
    simulator_thread.start()
    threads.append(simulator_thread)
