from math import *
from servo3 import Servo
from machine import Pin, PWM
from time import sleep

led = Pin("LED", Pin.OUT)
s = Servo(pin=13)

# angles en radians
angles = [0, math.pi/6, math.pi/4, math.pi/2, 2*math.pi/3, math.pi]
angle_MPU = [0, math.pi/4, math.pi/2, -math.pi/4, -math.pi/2, 0]
for a in angle_MPU:
    led.on()
    s.move(a)
    print("Move to {:.2f} rad".format(s.get_current_angle()))
    sleep(1)
led.off()












