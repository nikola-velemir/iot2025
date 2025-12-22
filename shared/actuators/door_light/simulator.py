from shared.actuators.door_light.actuator import DoorLightSensor
from shared.logger.logger import log


def run_door_light_sensor_simulator(light_sensor: DoorLightSensor, stop_event):
    """Blocking input loop for manual LED control."""
    while not stop_event.is_set():
        try:
            line = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            stop_event.set()
            break

        if not line:
            continue

        if line == "q":
            stop_event.set()
            break

        if line == "led on":
            light_sensor.light.turn_on()
            log("[CMD] LED turned ON")
        elif line == "led off":
            light_sensor.light.turn_off()
            log("[CMD] LED turned OFF")
        else:
            log(f"[CMD] Unknown command: {line}")
