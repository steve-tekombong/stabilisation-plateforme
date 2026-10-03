from machine import I2C
from math import atan2, sqrt

class MPU6050:

    def __init__(self, i2c, addr=0x68):

        self.i2c = i2c
        self.addr = addr

        self.i2c.writeto_mem(addr, 0x6B, b'\x00')

    def read_accel(self):

        data = self.i2c.readfrom_mem(self.addr, 0x3B, 6)

        ax = (data[0] << 8 | data[1])
        ay = (data[2] << 8 | data[3])
        az = (data[4] << 8 | data[5])

        if ax > 32767: ax -= 65536
        if ay > 32767: ay -= 65536
        if az > 32767: az -= 65536

        ax /= 16384
        ay /= 16384
        az /= 16384

        return ax, ay, az

    def pitch_roll(self):

        ax, ay, az = self.read_accel()

        pitch = atan2(ax, sqrt(ay*ay + az*az))
        roll = atan2(ay, sqrt(ax*ax + az*az))

        return pitch, roll