from machine import Pin, PWM
import math

class Servo:

    def __init__(self, pin, min_us=500, max_us=2500, angle_range_deg=180):

        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)

        self.min_us = min_us
        self.max_us = max_us
        self.angle_range = math.radians(angle_range_deg)

        self.current_angle = 0

    def _us_to_duty(self, us):

        period_us = 20000
        return int(us * 65535 / period_us)

    def move_rad(self, angle):

        angle = min(self.angle_range, angle)

        us = self.min_us + (self.max_us - self.min_us) * (angle / self.angle_range)

        self.pwm.duty_u16(self._us_to_duty(us))

        self.current_angle = angle 

    def get_current_angle(self):

        return self.current_angle