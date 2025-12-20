from sensors.door_light.sensor import DoorLightSensor


def run_door_light_sensor_simulator(delay, light_sensor:DoorLightSensor, stop_event):
    light = light_sensor.light

    while not stop_event.is_set():
        light.turn_on()
        if stop_event.wait(delay):
            break

        light.turn_off()
        if stop_event.wait(delay):
            break
