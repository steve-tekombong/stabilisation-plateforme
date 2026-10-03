
<div align="center">
  <img src="docs/Images/Plateforme-1.jpeg" width="500" alt="Plateforme de stabilisation TIPE">
  <br>
  <h1> Conception et stabilisation active d'une plateforme </h1>
</div>


## Contexte et objectifs

Le projet global s'inspire des systèmes d'amortissement du génie civil, comme la tour Taipei 101, et de la compensation de la houle pour les navires. Notre rôle s'est concentré sur le développement informatique et le traitement des signaux pour maintenir la plateforme horizontale malgré les perturbations. L'objectif logiciel est de traiter les données d'un capteur inertiel MPU-6050. Ensuite, il faut piloter des servomoteurs avec un microcontrôleur pour compenser l'inclinaison de la maquette. La logique globale est gérée par une boucle d'asservissement PID.

## Architecture logicielle (dossier src)

Le code embarqué tourne sur une carte Raspberry Pi Pico WH et est développé en MicroPython.

- **Traitement mathématique** : L'algorithme utilise les quaternions pour calculer les angles d'Euler.
- **Filtrage** : Un filtre complémentaire permet de fusionner les données de l'accéléromètre et du gyroscope, ce qui élimine le bruit et la dérive du capteur.
- **Asservissement** : Le correcteur PID calcule la commande à envoyer aux moteurs pour corriger l'écart angulaire, avec un temps d'échantillonnage constant (cycles) pour assurer la stabilité.
- **Actionnement** : Les corrections sont générées sous forme de signaux PWM envoyés aux servomoteurs de la structure.

## Analyse des résultats (dossier data_analyses) 

Pendant que le système fonctionne, le microcontrôleur envoie les données télémétriques en temps réel sur le port série. Des scripts Python récupèrent ces informations avec la bibliothèque PySerial et les stockent automatiquement sous forme de fichiers CSV. Pour fluidifier l'exploitation, tout le système de traitement a été automatisé : il suffit d'un simple clic pour exécuter le script qui lit les données, les traite et génère instantanément les graphiques 'matplotlib' comparant l'inclinaison brute et l'angle corrigé par le servo.Cette automatisation a grandement facilité l'analyse de l'efficacité de la boucle et l'ajustement expérimental des coefficients Kp et Ki du correcteur.Pour valider la robustesse du code, les tests ont été réalisés sur une plateforme de Stewart simulant des trajectoires dynamiques (séismes, houle).

## Documentation

- [Synthèse scientifique du TIPE](docs/Synthèse_scientifique_du_TIPE.pdf)
- [Présentation du TIPE](docs/Présentation_TIPE.pdf)
- [Images](docs/Images)

## Répartition du travail

Ce projet a été réalisé en binôme avec Clarence Jutier. Ma contribution s'est principalement concentrée sur le système embarqué, le traitement des données. La conception mécanique et la CAO de la plateforme ont principalement été réalisées par Clarence Jutier. Nous avons étudié ensemble l'asservissement PID et l'analyse expérimentale.

---
Steve TEKOMBONG
