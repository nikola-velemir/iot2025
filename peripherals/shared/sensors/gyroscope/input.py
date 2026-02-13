from abc import ABC, abstractmethod


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
        # Initialize I2C connection for MPU6050 or similar

    def read_gyro_data(self):
        # Todo: Read from I2C bus
        return 0.1, -0.05, 0.02

    def is_simulated(self) -> bool:
        return False