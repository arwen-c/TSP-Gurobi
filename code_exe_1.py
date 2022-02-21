from cmath import cos
from math import dist
from numpy import real
import pandas as pd
import math
import numpy as np

from firstdoc import *
from opti_test_amelie import ajout_domicile, optimisation_1

# Entrée - TO DO
# chemin d'accès à l'excel de données
path = 'InstanceItalyV1.xlsx'

# Corps du code


# Extraction des données
EmployeesDico, TasksDico = extraction_data(path)

# définition des petites variables
nbre_taches = len(TasksDico)
nbre_employe = len(EmployeesDico)
nbre_taches_tot = nbre_taches+2*nbre_employe

# ajout des tâches de départ et d'arrivée factices
#### ATTENTION : TasksDico comporte désormais les taches factices ####
TasksDico = ajout_domicile(TasksDico, EmployeesDico)

# Calcul de la matrice des distances Distance
tab_distance = matrice_distance(TasksDico)

# Création de Capacité, Durée, Début et Fin
Capacite = matriceCompetences(EmployeesDico, TasksDico)
Duree = vecteur_duree_tache(TasksDico)
Debut = vecteurOuvertures(TasksDico)
Fin = vecteurFermetures(TasksDico)

# Optimisation gurobi
solution = optimisation_1(Capacite, nbre_employe,
                          nbre_taches, tab_distance, Duree, Debut, Fin)

# Création des données
creation_fichier(path, 1, solution[0], solution[1], EmployeesDico)
