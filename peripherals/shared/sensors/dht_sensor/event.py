from dataclasses import dataclass


@dataclass

class DHTEvent:
    temp : float
    humidity : float
    sensor_name : str