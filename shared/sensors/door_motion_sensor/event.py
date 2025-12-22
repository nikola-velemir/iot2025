from dataclasses import dataclass

@dataclass(frozen=True)
class MotionStateChanged:
    motion_detected: bool
