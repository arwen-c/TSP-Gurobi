# Import de modules
import time
import copy

# Import des fonctions permettant la résolution
from usefulFunctions2 import *
from opti2 import ajoutTachesFictives, optimisation2

# Entrée - A MODIFIER
# chemin d'accès à l'excel de données
path = 'Phase2/InstancesV2/InstanceAustraliaV2.xlsx'


# Corps du code


# Extraction des données
EmployeesDico, EmployeesUnavailDico, TasksDico, TasksUnavailDico = extractionData(
    path)

# Définition des nombres de tâches réelles
nbre_taches = len(TasksDico)
nbre_employe = len(EmployeesDico)
nbreIndispoEmploye = len(EmployeesUnavailDico)

# Ajout de tâches de départ et d'arrivée (tâches factices)
#### ATTENTION : TasksDico comporte désormais les taches factices ####
TasksDicoNotModified=copy.deepcopy(TasksDico)
TasksDico = ajoutTachesFictives(
<<<<<<< HEAD
    TasksDico, EmployeesDico, EmployeesUnavailDico, TasksUnavailDico)
=======
    TasksDico, EmployeesDico, EmployeesUnavailDico)

>>>>>>> main
# Calcul de la matrice des distances Distance
tab_distance = matriceDistance(TasksDico)

# Création de Capacité, Durée, Début et Fin

# matrice de booléens. Vaut 1 en position [n,i] si l'employé n est capable d'effectuer la tache i, 0 sinon
Capacite = matriceCompetences(EmployeesDico, TasksDico)
# liste des durées des tâches
Duree = vecteurDurees(TasksDico)
# liste des début d'ouverture des tâches
Debut = vecteurOuvertures(TasksDico, TasksUnavailDico)
# liste des fins d'ouverture des tâches
Fin = vecteurFermetures(TasksDico, TasksUnavailDico)

debutTemps = time.time()


# Optimisation gurobi
borne = 1000
solution = optimisation2(Capacite, nbre_employe, nbre_taches, nbreIndispoEmploye,
                         tab_distance, Duree, Debut, Fin, EmployeesDico, TasksDico, borne)
# affichage multi objectif
print("Valeur fonction objectif : {} avec comme contrainte sur l'autre fonction objectif : {}".format(
    solution[3], solution[4]))

finTemps = time.time()
# print(finTemps - debutTemps)

# print("L :{}".format(solution[2]))

# Création du fichier solution au format txt
<<<<<<< HEAD
creationFichier(path, 1, solution[0], solution[1], TasksDico, EmployeesDico)
=======
creationFichier(path, 2, solution[0], solution[1], solution[2], TasksDicoNotModified, EmployeesDico)
>>>>>>> main
