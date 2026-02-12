from dataclasses import dataclass
import time

@dataclass(frozen=True)
class AlarmActivated:
    time : float = time.time()

@dataclass(frozen=True)
class AlarmDeactivated:
    time : float = time.time()


