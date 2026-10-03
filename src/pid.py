import time

class PID:
    # Constantes de mode et de direction
    MANUAL = 0
    AUTOMATIC = 1
    DIRECT = 0
    REVERSE = 1

    def __init__(self, input_val=0.0, output_val=0.0, setpoint_val=0.0, kp=0.0, ki=0.0, kd=0.0, direction=DIRECT):
        
        # Variables de travail
        self.Input = input_val
        self.Output = output_val
        self.Setpoint = setpoint_val
        
        self.ITerm = 0.0
        self.lastInput = input_val
        
        self.kp = 0.0
        self.ki = 0.0
        self.kd = 0.0
        
        self.SampleTime = 1000  # 1 sec (en millisecondes)
        self.outMin = 0.0
        self.outMax = 255.0     # Par défaut pour du PWM Arduino
        
        self.inAuto = False
        self.controllerDirection = direction
        
        self.lastTime = self._millis()
        
        self.SetOutputLimits(self.outMin, self.outMax)
        self.SetTunings(kp, ki, kd)

    def _millis(self):
        """Équivalent de la fonction millis() d'Arduino"""
        return int(time.time() * 1000)

    def Compute(self):
        """Méthode principale à appeler en boucle [3]"""
        if not self.inAuto:
            return False

        now = self._millis()
        timeChange = now - self.lastTime

        if timeChange >= self.SampleTime:
            # Calcul de toutes les variables d'erreur [3]
            error = self.Setpoint - self.Input
            
            # Intégration (ITerm) avec anti-windup intégré [3, 6]
            self.ITerm += (self.ki * error)
            if self.ITerm > self.outMax:
                self.ITerm = self.outMax
            elif self.ITerm < self.outMin:
                self.ITerm = self.outMin
                
            # Calcul du dInput pour éviter le Derivative Kick [3, 7]
            dInput = self.Input - self.lastInput

            # Calcul de la sortie PID [3]
            self.Output = (self.kp * error) + self.ITerm - (self.kd * dInput)

            # Clamp de la sortie [3]
            if self.Output > self.outMax:
                self.Output = self.outMax
            elif self.Output < self.outMin:
                self.Output = self.outMin

            # Sauvegarde des variables pour le prochain cycle [3]
            self.lastInput = self.Input
            self.lastTime = now
            return True
            
        return False

    def SetTunings(self, Kp, Ki, Kd):
        """Modification des paramètres à la volée [8, 9]"""
        if Kp < 0 or Ki < 0 or Kd < 0:
            return

        SampleTimeInSec = self.SampleTime / 1000.0

        self.kp = Kp
        self.ki = Ki * SampleTimeInSec
        self.kd = Kd / SampleTimeInSec

        # Prise en compte du sens de contrôle (Direct ou Reverse) [9]
        if self.controllerDirection == self.REVERSE:
            self.kp = -self.kp
            self.ki = -self.ki
            self.kd = -self.kd

    def SetSampleTime(self, NewSampleTime):
        """Ajustement du temps d'échantillonnage [5, 9]"""
        if NewSampleTime > 0:
            ratio = float(NewSampleTime) / float(self.SampleTime)
            self.ki *= ratio
            self.kd /= ratio
            self.SampleTime = int(NewSampleTime)

    def SetOutputLimits(self, Min, Max):
        """Définition des limites pour éviter le Reset Windup [6, 9]"""
        if Min > Max:
            return
        self.outMin = Min
        self.outMax = Max

        if self.Output > self.outMax:
            self.Output = self.outMax
        elif self.Output < self.outMin:
            self.Output = self.outMin

        if self.ITerm > self.outMax:
            self.ITerm = self.outMax
        elif self.ITerm < self.outMin:
            self.ITerm = self.outMin

    def SetMode(self, Mode):
        """Bascule entre Manuel et Automatique avec transfert sans à-coup [9, 10]"""
        newAuto = (Mode == self.AUTOMATIC)
        if newAuto and not self.inAuto:
            # On vient de passer de Manuel à Auto, on initialise [9]
            self.Initialize()
        self.inAuto = newAuto

    def Initialize(self):
        """Initialisation des variables pour éviter un bond (bump) à l'allumage [9, 11]"""
        self.lastInput = self.Input
        self.ITerm = self.Output
        if self.ITerm > self.outMax:
            self.ITerm = self.outMax
        elif self.ITerm < self.outMin:
            self.ITerm = self.outMin
            
    def SetControllerDirection(self, Direction):
        """Définit si le processus est à action directe ou inverse [3, 12]"""
        self.controllerDirection = Direction

"""
Comment l'utiliser dans ton programme principal ?
Contrairement à l'Arduino où les variables globales "flottent", ici tu dois lire les capteurs, mettre à jour la propriété Input de l'objet, exécuter Compute(), puis récupérer la nouvelle valeur Output pour l'envoyer à tes servomoteurs.
Voici un exemple de boucle d'utilisation :
# 1. Initialisation du contrôleur
mon_pid = PID(kp=2.0, ki=5.0, kd=1.0)
mon_pid.SetMode(PID.AUTOMATIC)
mon_pid.SetSampleTime(10) # Boucle toutes les 10ms pour une grande réactivité
mon_pid.SetOutputLimits(-90.0, 90.0) # Par exemple, l'angle max de tes servomoteurs
mon_pid.Setpoint = 0.0 # On veut que la plateforme soit parfaitement à plat

try:
    while True:
        # 2. Lire la valeur actuelle du capteur (ton MPU-6050)
        angle_actuel = lire_capteur_mpu() 
        
        # 3. Transmettre l'information au PID
        mon_pid.Input = angle_actuel
        
        # 4. Faire calculer le PID (Compute retourne True si assez de temps s'est écoulé)
        if mon_pid.Compute():
            # 5. Récupérer l'action de correction
            correction = mon_pid.Output
            
            # 6. Appliquer l'action aux servomoteurs
            appliquer_au_servomoteur(correction)

        # Petite pause pour ne pas surcharger le CPU du Raspberry Pi Pico
        time.sleep(0.001) 

except KeyboardInterrupt:
    print("Arrêt du stabilisateur")
"""
