import time
import sys
from guppy import hpy


from usefulFunctions1 import *
from opti1 import ajoutDomicile, optimisation1

# Entrée - A MODIFIER
# chemin d'accès à l'excel de données
path = 'Phase1/InstancesV1/InstanceBordeauxV1.xlsx'


### CORPS DU CODE ###


# Extraction des données
employeesDico, tasksDico = extractionData(path)

# Définition de variables
nbreTaches = len(tasksDico)
nbreEmploye = len(employeesDico)

# Ajout de tâches de départ et d'arrivée (tâches factices)
#### ATTENTION : TasksDico comporte désormais les taches factices ####
tasksDico = ajoutDomicile(tasksDico, employeesDico)

# Calcul de la matrice des distances Distance
tabDistance = matriceDistance(tasksDico)

# Création de Capacité, Durée, Début et Fin

# matrice de booléens. Vaut 1 en position [n,i] si l'employé n est capable d'effectuer la tache i, 0 sinon
capacite = matriceCompetences(employeesDico, tasksDico)
# liste des durées des tâches
duree = vecteurDurees(tasksDico)
# liste des début d'ouverture des tâches
debut = vecteurOuvertures(tasksDico)
# liste des fins d'ouverture des tâches
fin = vecteurFermetures(tasksDico)

debutTemps = time.time()


# Optimisation gurobi
solution = optimisation1(capacite, nbreEmploye,
                         nbreTaches, tabDistance, duree, debut, fin)

finTemps = time.time()


performances1(finTemps-debutTemps, sys.getsizeof(capacite) + sys.getsizeof(duree)+sys.getsizeof(debut)+sys.getsizeof(fin) +
              sys.getsizeof(tabDistance), hpy().heap().size, path)

# Création du fichier solution au format txt
creationFichier(path, 1, solution[0], solution[1], employeesDico)

print("\nLa distance totale parcourue par l'ensemble des employés est de : {:.2f} km \nLa durée totale des tâches réalisées par l'ensemble des employés : {:.0f} h".format(
    solution[2], solution[3]/60))

# pb corrigé : erreur "permission denied" : ne pas avoir le fichier d'ouvert en parallèle !
