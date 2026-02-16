from abc import ABC, abstractmethod

from RPi import GPIO

from shared.logger.logger import log


class BuzzerOutput(ABC):
    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass
    
class SimulatedBuzzer(BuzzerOutput):
    def __init__(self):
        self._state = False

    def on(self):
        if not self._state:
            self._state = True
            log("Buzzer ON!")

    def off(self):
        if self._state:
            self._state = False
            log("Buzzer OFF!")

    def is_simulated(self) -> bool:
        return False

class GpioBuzzer(BuzzerOutput):
    def __init__(self, gpio_pin, duty_cycle=50, frequency = 200):
        self.gpio_pin = gpio_pin
        self._frequency = frequency
        self._duty_cycle = duty_cycle
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        self._buzz_obj = GPIO.PWM(self.gpio_pin, self._frequency)

    def on(self):
        self._buzz_obj.start(self._duty_cycle)
        log("Buzzer ON!")

    def off(self):
        self._buzz_obj.stop()
        log("Buzzer OFF!")


    def is_simulated(self) -> bool:
        return False

