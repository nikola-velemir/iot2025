from abc import ABC, abstractmethod

from RPi import GPIO

from shared.logger.logger import log

# Output abstraction
class BRGBOutput(ABC):
    @abstractmethod
    def is_simulated(self) -> bool:
        pass

    @abstractmethod
    def set_color(self, color: str):
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class SimulatedBRGBOutput(BRGBOutput):
    def __init__(self, name: str):
        self.name = name
        self.current_color = "OFF"

    def is_simulated(self) -> bool:
        return True

    def set_color(self, color: str):
        self.current_color = color
        log(f"[{self.name}] changed color to {color}")

    def turn_on(self):
        self.current_color = "WHITE"
        log(f"[{self.name}] turned ON")

    def turn_off(self):
        self.current_color = "OFF"
        log(f"[{self.name}] turned OFF")


class GpioBRGBOutput(BRGBOutput):
    def __init__(self, name: str, red_pin: int, green_pin: int, blue_pin: int):
        self.name = name
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.current_color = "OFF"

        # set pins as outputs
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)

    def is_simulated(self) -> bool:
        return False

    def set_color(self, color: str):
        self.current_color = color
        log(f"[GPIO] {self.name} changed color to {color}")

        if color == "WHITE":
            self.white()
        if color == "RED":
            self.red()
        if color == "GREEN":
            self.green()
        if color == "BLUE":
            self.blue()
        if color == "YELLOW":
            self.yellow()
        if color == "PURPLE":
            self.purple()
        if color == "CYAN":
            self.cyan()

    def turn_on(self):
        self.current_color = "WHITE"
        log(f"[GPIO] {self.name} turned ON")

    def turn_off(self):
        self.current_color = "OFF"
        log(f"[GPIO] 🌑 {self.name} turned OFF")

        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def white(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def red(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def green(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def blue(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def yellow(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.LOW)

    def purple(self):
        GPIO.output(self.red_pin, GPIO.HIGH)
        GPIO.output(self.green_pin, GPIO.LOW)
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def cyan(self):
        GPIO.output(self.red_pin, GPIO.LOW)
        GPIO.output(self.green_pin, GPIO.HIGH)
        GPIO.output(self.blue_pin, GPIO.HIGH)
