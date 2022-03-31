# Import de modules
import time
import sys
from guppy import hpy
import copy

# Import des fonctions permettant la résolution
from usefulFunctions2 import *
from opti2 import ajoutTachesFictives, optimisation2
from epsilonContrainte import plotSolutions1, plotSolutions2, epsilonContrainte
from graphique2 import afficher

# Entrée - A MODIFIER
# chemin d'accès à l'excel de données

ville = 'Bordeaux'
path = 'Phase2/InstancesV2/Instance'+ville+'V2.xlsx'

print(path)

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
TasksDicoNotModified = copy.deepcopy(TasksDico)
TasksDico = ajoutTachesFictives(
    TasksDico, EmployeesDico, EmployeesUnavailDico)

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
# liste des disponibilités des tâches
dispos = [dispostache(tasknb, TasksDico, TasksUnavailDico)
          for tasknb in range(len(TasksDico))]
debutTemps = time.time()


# Optimisation gurobi

# choisir 1 ou 2, en fonction de la fonction que l'on souhaite optimiser
fonctionObjectif = 3
# choisir la valeur de la borne pour l'autre fonction objectif (qui sera traitée comme une contrainte dans le solveur)
borne = 10000  # attention à mettre une valeur cohérente
solution = optimisation2(Capacite, nbre_employe, nbre_taches, nbreIndispoEmploye,
                         tab_distance, Duree, EmployeesDico, TasksDico, borne, fonctionObjectif, dispos)
# affichage multi objectif
print("Valeur fonction objectif : {} avec comme contrainte sur l'autre fonction objectif : {}".format(
    solution[3], solution[4]))


# Pour tracer les graphiques des algorithmes epsilon Contraintes
# fonctionObjectif = 1
# plotSolutions1(fonctionObjectif, *epsilonContrainte(2, Capacite, nbre_employe,
#                                      nbre_taches, nbreIndispoEmploye, tab_distance, Duree, Debut, Fin, EmployeesDico, TasksDico))

# plotSolutions2(Capacite, nbre_employe, nbre_taches, nbreIndispoEmploye,
#                tab_distance, Duree, Debut, Fin, EmployeesDico, TasksDico)

finTemps = time.time()
# print(finTemps - debutTemps)
# performances2(finTemps-debutTemps, sys.getsizeof(Capacite) + sys.getsizeof(Duree)+sys.getsizeof(Debut)+sys.getsizeof(Fin) +
#               sys.getsizeof(tab_distance), hpy().heap().size, path)

# Création du fichier solution au format txt
creationFichier(path, 2, solution[0], solution[1],
                solution[2], TasksDicoNotModified, EmployeesDico)

creationFichierPlottable(path,2,solution[0],solution[1],solution[2],TasksDicoNotModified,EmployeesDico,EmployeesUnavailDico)
# Affichage :
afficher(ville)
