from abc import ABC, abstractmethod
import random

class MotionInput(ABC):
    @abstractmethod
    def is_motion(self) -> bool:
        """Return True if motion is detected"""
        pass




class SimulatedMotionInput(MotionInput):
    def __init__(self):
        self._motion = False

    def is_motion(self) -> bool:
        return self._motion

    def simulate_motion(self):
        """Randomly decide motion state"""
        self._motion = random.choice([True, False])
