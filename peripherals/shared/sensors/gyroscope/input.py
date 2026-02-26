from abc import ABC, abstractmethod

from .MPU6050 import MPU6050
from mpu6050 import MPU6050

class GyroscopeInput(ABC):
    @abstractmethod
    def read_gyro_data(self):
        """Returns (x, y, z) angular velocity"""
        pass

    @abstractmethod
    def is_simulated(self) -> bool:
        pass


class SimulatedGyroscope(GyroscopeInput):
    def __init__(self):
        self.x, self.y, self.z = 0.0, 0.0, 0.0

    def set_data(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def read_gyro_data(self):
        return self.x, self.y, self.z

    def is_simulated(self) -> bool:
        return True


class GpioGyroscope(GyroscopeInput):
    def __init__(self, i2c_address=0x68):
        self.address = i2c_address
        self._mpu = MPU6050(self.address)

    def read_gyro_data(self):
        """
        Returns gyro rotation in degrees per second as a dict: {'x': .., 'y': .., 'z': ..}
        """
        data = self._mpu.get_gyro_data()  # {'x': .., 'y': .., 'z': ..}
        print("Gyro:", data)
        return data

    def read_accel_data(self):
        """
        Returns acceleration in g as a dict: {'x': .., 'y': .., 'z': ..}
        """
        data = self._mpu.get_accel_data()
        return data

    def is_simulated(self) -> bool:
        return False