from cmath import cos
from math import *
from numpy import real
from gurobipy import *
# from Phase_1.epsilonContrainte import plotSolutions1
from epsilonContrainte import epsilonContrainte, plotSolutions1, plotSolutions2


from firstdoc import *
from opti_1 import ajout_domicile, optimisation_1

# Entrée - A MODIFIER
# chemin d'accès à l'excel de données
path = 'Phase_2/InstancesV2/InstanceBordeauxV2.xlsx'
#path = 'Phase_1/InstancesV1/InstanceBordeauxV1.xlsx'

# Corps du code


# Extraction des données
EmployeesDico, TasksDico = extraction_data(path)

# Définition de variables
nbre_taches = len(TasksDico)
nbre_employe = len(EmployeesDico)
nbre_taches_tot = nbre_taches + 2*nbre_employe

# Ajout de tâches de départ et d'arrivée (tâches factices)
#### ATTENTION : TasksDico comporte désormais les taches factices ####
TasksDico = ajout_domicile(TasksDico, EmployeesDico)

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

# ajout du nombre de tâches réelles pour l'opti bi-objectifs
ntR = len(TasksDico)

borne = math.inf
# Optimisation gurobi
solution = optimisation_1(Capacite, nbre_employe,
                          nbre_taches, tab_distance, Duree, Debut, Fin, ntR, borne, 2)

# affichage multi objectif
print("Valeur fonction objectif : {} avec comme contrainte sur l'autre fonction objectif : {}".format(
    solution[2], solution[3]))


# # Création du fichier solution au format txt
# creation_fichier(path, 1, solution[0], solution[1], EmployeesDico)


def epsilon_contrainte():
    epsilon = 10
    borne = 1000
    valeurObjectifs = []
    valeurBornes = []
    possible = True
    while possible:
        try:
            solution = optimisation_1(Capacite, nbre_employe,
                                      nbre_taches, tab_distance, Duree, Debut, Fin, ntR, borne, 1)
            borne = solution[3]-epsilon
            valeurObjectifs.append(solution[2])
            valeurBornes.append(solution[3])
            break
        except gurobipy.GurobiError:  # si on ne trouve plus de solution avec la borne imposée sur l'une des fonctions objectifs
            possible = False
        # solution[3] = f1(solution)
    return valeurObjectifs, valeurBornes


# print(epsilon_contrainte())
# print("La liste des valeurs objetifs est : {} et la liste des valeurs de l'autre fonction objectif est : {}".format(
#     epsilon_contrainte()[0], epsilon_contrainte()[1]))

# print(epsilonContrainte(1, Capacite, nbre_employe,
#                         nbre_taches, tab_distance, Duree, Debut, Fin, ntR))

# plotSolutions1(*epsilonContrainte(1, Capacite, nbre_employe,
#                                  nbre_taches, tab_distance, Duree, Debut, Fin, ntR))

# plotSolutions2(Capacite, nbre_employe, nbre_taches,
#                tab_distance, Duree, Debut, Fin, ntR)
