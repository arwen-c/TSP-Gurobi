from cmath import cos
from math import dist
from click import pause
from numpy import real


from firstdoc import *
from opti_1 import ajout_domicile, optimisation_1, pauseDej

# Entrée - A MODIFIER
# chemin d'accès à l'excel de données
path = 'Phase_1/InstancesV1/InstanceBordeauxV1.xlsx'


# Corps du code


# Extraction des données
EmployeesDico, TasksDico = extraction_data(path)

# Définition de variables
nbre_taches = len(TasksDico)
nbre_employe = len(EmployeesDico)
nbre_taches_tot = nbre_taches + 3*nbre_employe

# Ajout de tâches de départ et d'arrivée (tâches factices)
#### ATTENTION : TasksDico comporte désormais les taches factices ####
TasksDico = ajout_domicile(TasksDico, EmployeesDico)
TasksDico= pauseDej(TasksDico, EmployeesDico)

# Calcul de la matrice des distances Distance
tab_distance = matrice_distance(TasksDico)

# Création de Capacité, Durée, Début et Fin

# matrice de booléens. Vaut 1 en position [n,i] si l'employé n est capable d'effectuer la tache i, 0 sinon
Capacite = matriceCompetences(EmployeesDico, TasksDico)
# liste des durées des tâches
Duree = vecteurDurees(TasksDico)
# liste des début d'ouverture des tâches
Debut = vecteurOuvertures(TasksDico)
# liste des fins d'ouverture des tâches
Fin = vecteurFermetures(TasksDico)

# Optimisation gurobi
solution = optimisation_1(Capacite, nbre_employe,
                          nbre_taches, tab_distance, Duree, Debut, Fin)

# Création du fichier solution au format txt
creation_fichier(path, 2, solution[0], solution[1], EmployeesDico)
