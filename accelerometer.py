from machine import Pin, I2C
import utime
import math

# MPU-6050 Registers and their addresses
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

class MPU6050_Accelerometer():
    def __init__(self, i2c):
        self.i2c = i2c
        self.mpu6050_init()

    def mpu6050_init(self):
        self.i2c.writeto_mem(MPU6050_ADDR, PWR_MGMT_1, b'\x00')

    # Read raw 16-bit value from a register
    def read_raw_data(self, addr):
        high = self.i2c.readfrom_mem(MPU6050_ADDR, addr, 1)[0]
        low = self.i2c.readfrom_mem(MPU6050_ADDR, addr + 1, 1)[0]
        value = (high << 8) | low
        if value > 32768:
            value -= 65536
        return value

    # Read accelerometer data
    def get_acceleration(self):
        acc_x = self.read_raw_data(ACCEL_XOUT_H)
        acc_y = self.read_raw_data(ACCEL_YOUT_H)
        acc_z = self.read_raw_data(ACCEL_ZOUT_H)
        return acc_x / 16384.0, acc_y / 16384.0, acc_z / 16384.0  # Convert to 'g'

    # Read gyroscope data
    def get_gyro(self):
        gyro_x = self.read_raw_data(GYRO_XOUT_H)
        gyro_y = self.read_raw_data(GYRO_YOUT_H)
        gyro_z = self.read_raw_data(GYRO_ZOUT_H)
        return gyro_x / 131.0, gyro_y / 131.0, gyro_z / 131.0  # Convert to deg/s

