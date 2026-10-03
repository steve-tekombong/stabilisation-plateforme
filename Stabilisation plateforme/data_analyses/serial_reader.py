import serial
import time
print("Initialisation système")
port = "COM4"   # adapter selon ton PC
baud = 115200
print("Démarage")
ser = serial.Serial(port, baud)
print("Go")

time.sleep(2)  # laisser la pico démarrer

C = open("C:\XboxGames\TIPE\MesurePID\CompteurPID.csv", "a")
C.write("allo" + "\n")
C.close()

C=open("C:\XboxGames\TIPE\MesurePID\CompteurPID.csv", "r")
L=C.readlines()
print(len(L))

f = open("C:\XboxGames\TIPE\MesurePID\MesurePID" + str(len(L)) +".csv", "w")

print("Enregistrement... Ctrl+C pour arrêter")

while True:

    line = ser.readline().decode().strip()

    print(line)

    f.write(line + "\n")



f.close()
ser.close()
