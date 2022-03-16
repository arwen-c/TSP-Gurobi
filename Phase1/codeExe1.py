from cmath import cos
from math import dist
from numpy import real
import time
import sys
from guppy import hpy


from usefulFunctions1 import *
from opti1 import ajoutDomicile, optimisation1

# Entrée - A MODIFIER
# chemin d'accès à l'excel de données
Path = 'Phase1/InstancesV1/InstancePolandV1.xlsx'


### CORPS DU CODE ###


# Extraction des données
EmployeesDico, TasksDico = extractionData(Path)

# Définition de variables
NbreTaches = len(TasksDico)
NbreEmploye = len(EmployeesDico)

# Ajout de tâches de départ et d'arrivée (tâches factices)
#### ATTENTION : TasksDico comporte désormais les taches factices ####
TasksDico = ajoutDomicile(TasksDico, EmployeesDico)

# Calcul de la matrice des distances Distance
TabDistance = matriceDistance(TasksDico)

# Création de Capacité, Durée, Début et Fin

# matrice de booléens. Vaut 1 en position [n,i] si l'employé n est capable d'effectuer la tache i, 0 sinon
Capacite = matriceCompetences(EmployeesDico, TasksDico)
# liste des durées des tâches
Duree = vecteurDurees(TasksDico)
# liste des début d'ouverture des tâches
Debut = vecteurOuvertures(TasksDico)
# liste des fins d'ouverture des tâches
Fin = vecteurFermetures(TasksDico)

Debut = time.time()


# Optimisation gurobi
Solution = optimisation1(Capacite, NbreEmploye,
                         NbreTaches, TabDistance, Duree, Debut, Fin)

Fin = time.time()


performances1(Fin-Debut, sys.getsizeof(Capacite) + sys.getsizeof(Duree)+sys.getsizeof(Debut)+sys.getsizeof(Fin) +
              sys.getsizeof(TabDistance), hpy().heap().size, Path)

# Création du fichier solution au format txt
creationFichier(Path, 1, Solution[0], Solution[1], EmployeesDico)

# pb corrigé : erreur "permission denied" : ne pas avoir le fichier d'ouvert en parallèle !
