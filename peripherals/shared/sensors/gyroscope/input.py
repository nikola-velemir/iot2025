from abc import ABC, abstractmethod

from .MPU6050 import MPU6050

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
        self._mpu = MPU6050(i2c_address)
        self._mpu.dmp_initialize()
        # Initialize I2C connection for MPU6050 or similar

    def read_gyro_data(self):
        gyro = self._mpu.get_rotation()   # returns (x, y, z)
        print(gyro)
        return gyro
    def read_accel_data(self):
        return self._mpu.get_acceleration()  # optional
    def is_simulated(self) -> bool:
        return False