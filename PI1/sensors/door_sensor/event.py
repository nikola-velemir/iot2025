import dataclasses


@dataclasses.dataclass(frozen=True)
class DoorStateChanged:
    is_open: bool