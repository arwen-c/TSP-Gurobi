# Import de modules
import time
# import sys
import copy

# Import des fonctions permettant la résolution
from usefulFunctions3 import *
from glouton import optiGlouton


# Entrée - A MODIFIER
# chemin d'accès à l'excel de données
path = 'Phase2/InstancesV2/InstanceAustraliaV2.xlsx'


# Corps du code


# Extraction des données
employesDico, indispoEmployesDico, tachesDico, indispoTachesDico = extractionData(
    path)

# Définition des nombres de tâches réelles
nbreTaches = len(tachesDico)
nbreIndispoEmploye = len(indispoEmployesDico)

# Ajout de tâches de départ et d'arrivée (tâches factices)
#### ATTENTION : tachesDico comporte désormais les taches factices ####
tachesDicoNonModifie = copy.deepcopy(tachesDico)
tachesDico = ajoutTachesFictives(tachesDico, employesDico, indispoEmployesDico)

# Calcul de la matrice des distances Distance
matDistance = matriceDistance(tachesDico)

# Création de Capacité, Durée, Début et Fin

# matrice de booléens. Vaut 1 en position [n,i] si l'employé n est capable d'effectuer la tache i, 0 sinon
capacite = matriceCompetences(employesDico, tachesDico)
# liste des durées des tâches
duree = vecteurDurees(tachesDico)
# liste des début d'ouverture des tâches
debut = vecteurOuvertures(tachesDico, indispoTachesDico)
# liste des fins d'ouverture des tâches
fin = vecteurFermetures(tachesDico, indispoTachesDico)

debutTemps = time.time()


# Optimisation gloutonne


solution = optiGlouton(capacite, matDistance, duree, debut, fin,
                       nbreTaches, employesDico, indispoEmployesDico, tachesDico)
# affichage multi objectif

print("Valeur fonction objectif : {} avec comme contrainte sur l'autre fonction objectif : {}".format(
    solution[3], solution[4]))


# Pour tracer les graphiques des algorithmes epsilon Contraintes
# fonctionObjectif = 1
# plotSolutions1(fonctionObjectif, *epsilonContrainte(2, Capacite, nbre_employe,
#                                      nbre_taches, nbreIndispoEmploye, tab_distance, Duree, Debut, Fin, employesDico, tachesDico))

# plotSolutions2(Capacite, nbre_employe, nbre_taches, nbreIndispoEmploye,
#                tab_distance, Duree, Debut, Fin, employesDico, tachesDico)

finTemps = time.time()
# print(finTemps - debutTemps)
# performances2(finTemps-debutTemps, sys.getsizeof(capacite) + sys.getsizeof(duree)+sys.getsizeof(debut)+sys.getsizeof(fin) + sys.getsizeof(matDistance), hpy().heap().size, path)

# Création du fichier solution au format txt
creationFichier(path, 3, solution[0], solution[1],
                solution[2], tachesDicoNonModifie, employesDico)
