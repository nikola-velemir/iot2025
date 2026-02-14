from abc import ABC, abstractmethod

from shared.logger.logger import log


class TimerOutput(ABC):
    @abstractmethod
    def display_time(self, minutes: int, seconds: int):
        """Display time in MM:SS format on 4-digit display"""
        pass

    @abstractmethod
    def clear(self):
        """Clear the display (for blinking effect)"""
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass


class SimulatedStopwatchOutput(TimerOutput):
    def __init__(self):
        self.current_display = "00:00"
        self.is_clear = False

    def display_time(self, minutes: int, seconds: int):
        self.current_display = f"{minutes:02d}:{seconds:02d}"
        self.is_clear = False
        log(f"[TIMER DISPLAY] {self.current_display}")

    def clear(self):
        self.is_clear = True
        log(f"[TIMER DISPLAY] ----")

    def is_simulated(self) -> bool:
        return True


class GpioStopwatchOutput(TimerOutput):
    def __init__(self, i2c_address=0x70):
        self.address = i2c_address


    def display_time(self, minutes: int, seconds: int):


        log(f"[GPIO TIMER] Displaying {minutes:02d}:{seconds:02d}")

    def clear(self):

        log(f"[GPIO TIMER] Display cleared")

    def is_simulated(self) -> bool:
        return False