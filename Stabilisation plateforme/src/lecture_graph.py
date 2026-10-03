# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 18:19:23 2026

@author: tekom
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 18:08:01 2026

@author: tekom
"""
from math import *
import numpy as np
import matplotlib.pyplot as plt

f=open("C:\XboxGames\TIPE\MesurePID\CompteurPID.csv", "r")
L=f.readlines()


data = np.loadtxt("C:\XboxGames\TIPE\MesurePID\MesurePID" + str(len(L)) +".csv", skiprows=1)


t = data[:,0]/1000
angle = data[:,1]
servo = data[:,2]
corr = data[:, 3]
Kp=data[:, 4]
Ki= data[:, 5]
Kd= data[:, 6]
Value_Ki= Ki[1]
Value_Kp= Kp[1]
Value_Kd= Kd[1]
angle_deg=[]
servo_deg=[]
t_reset=[]

for i in range(len(angle)):
    angle_deg.append(180*(angle[i])/pi)
    servo_deg.append(180*servo[i]/pi)
    t_reset.append(t[i]- 8.605)

plt.figure(1)
plt.plot(t_reset, angle_deg, 'b', label="Angle MPU")
plt.plot(t_reset, servo_deg, 'r', label="Angle Servo avec Kp={}, Ki={}, Kd={}". format(Value_Kp, Value_Ki, Value_Kd))
plt.xlabel("Temps (s)")
plt.ylabel("Angle (deg)")
plt.legend(loc='upper left')
plt.grid()
plt.show()

plt.figure(2)

plt.plot(t, corr, 'g', label="différence". format(Value_Kp, Value_Ki, Value_Kd))
"""
plt.xlabel("temps (s)")
plt.ylabel("angle (rad)")
plt.legend()
plt.grid()

"""