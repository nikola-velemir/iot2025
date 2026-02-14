import dataclasses


@dataclasses.dataclass(frozen=True)
class DoorStateChanged:
    is_open: bool


@dataclasses.dataclass(frozen=True)
class DoorOpenTooLong:
    sensor_name: str
