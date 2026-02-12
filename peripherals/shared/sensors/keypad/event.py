import dataclasses


@dataclasses.dataclass(frozen=True)
class KeyPressed:
    key: str