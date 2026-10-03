from machine import Pin, SoftI2C
from math import *
from time import sleep_ms, ticks_ms, ticks_diff
from servo3 import Servo
from mp_simple import MPU6050

i2c = SoftI2C(scl=Pin(21), sda=Pin(20), freq=400000)
mpu = MPU6050(i2c)
servo = Servo(13)

kp=30
ki=10

setpoint=0
before = 0
last_error=0
last_pitch=0

t0=0

alpha = 0.9

def conv(x):
    return x*pi/180

def compute(input_val, before, last_error):

    now = ticks_ms()
    dt = ticks_diff(now, last_time) / 1000
    
   
    error = setpoint - input_val
    
    output =  before -  kp * last_error + (kp + ki*dt)*error
    return output, error

while True:
    pitch, roll = mpu.pitch_roll()
    
    
    last_time = ticks_ms()
    correction, error = compute(pitch, before, last_error) 
    
    if correction == 0:
        print("bite")
        
    servo_angle = pitch
    
    servo.move(round(servo_angle, 3))
    t = ticks_diff(ticks_ms(), t0)
    print("{} {} {} {} {} {} \n".format(t, pitch, -servo_angle, conv(correction), kp, ki))
    
    last_error = error
    before = correction
    sleep_ms(100)
    
    








"""
    pitch_filtre = alpha * pitch_filtre + (1 - alpha) * pitch
    mon_pid.Input = pitch_filtre
    
    if correction >= math.pi/2:
        servo.move_rad(math.pi/2)
    else:
        servo.move_rad(radians(correction))
    
while True:

    pitch, roll = mpu.pitch_roll()
    #pitch_filtre = alpha
    #pitch_filtre = alpha * pitch_filtre + (1 - alpha) * pitch
    mon_pid.Input = pitch   
    
    mon_pid.Compute()  

    correction = mon_pid.Output

       
    servo_angle = pitch
    if pitch > radians(20):
        servo.move_rad(pitch-pi/4)
        
    servo.move_rad(servo_angle)
    
        
    t = ticks_diff(ticks_ms(), t0)
    print("{} {} {} {} \n".format(t, pitch, -servo_angle, pitch- servo.get_current_angle() + pi/2))


    sleep_ms(100)
    #servo_angle = radians(correction)
    #print("{} {} {} {} {} {} {} \n".format(t, pitch, servo.get_current_angle()-pi/2, pitch+servo.get_current_angle()-pi/2, Kp, Ki, Kd))

    #print(pitch,  pitch+servo.get_current_angle() , servo.get_current_angle())





"""



   