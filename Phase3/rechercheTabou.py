from distutils.log import ERROR
from re import M
from glouton import *
import numpy as np
from usefulFunctions3 import * 

# question : comment caractériser une solution ? Par la matrice des X ? Ca rend la comparaison entre plusieurs solutions assez laborieuse pour de grandes instances
# quel critère d'arrêt ? pour une première version, utilisation d'un nombre d'itération maximum. Par la suite, on peut améliorer le programme en utilisant un nombre max d'itération depuis la dernière mise à jour d'un minimum (dernier ajout à la liste tabou)
# d'autres améliorations, notamment sur la tailleMemoire sont proposées dans le poly de métaheuristique


def rechercheTabou(solInit, capacite, matDistance, duree, debut, fin, nbreTaches, employeesDico, indispoDico, tachesDico, tailleMemoire):

    ###### Étape 0: La première étape consiste à créer une solution initiale afin que l'algorithme puisse la parcourir et en trouver une meilleure.
    # La solution initiale peut être considérée comme le point de départ de l'algorithme, dans la plupart des cas, 
    # cette solution initiale est attribuée au hasard, cependant, nous allons utiliser une solution retournée par l'algorithme glouton.

    

    ###### Étape 1: Maintenant que nous avons la solution initiale, l'étape suivante consiste à créer la liste des solutions candidates à partir 
    # de la solution courante 𝕊 (solution initiale à l'itération 0), nous appelons ces solutions voisins ou voisinage de 𝕊. 
    # Pour trouver les solutions voisines à partir de la solution courante 𝕊, nous devons définir ce qu'on appelle une fonction de voisinage, 
    # sous cette fonction chaque solution 𝕊 a un sous-ensemble de solutions associé. La fonction de voisinage peut faire l'une de ces opérations :
    # 1. Inserer une tˆache non effectu ́ee dans un trous du planning d’un employ ́e
    # 2. Supprimer une tˆache du planning d’un employ ́e
    # 3. Intervertir deux arrˆetes d’un mˆeme employ ́e
    # 4. changer d’employ ́e pour une tˆache donn ́ee
    # 5. changer l’heure de la pause d ́ejeuner
    # 6. Faire une tˆache qui n’est pas faite `a la place d’une autre tˆache

    

    ###### Étape 2: À partir de la liste des solutions de quartier créée à l'étape 1, 
    # nous choisissons la meilleure solution admissible (non tabou ou répondant aux critères d'aspiration) en vérifiant chaque solution


    ###### Étape 3: Vérifiez les critères d'arrêt définis,
    #  cela peut être le nombre maximum d'itérations atteintes ou le temps d'exécution, si les critères d'arrêt ne sont pas remplis,
    #  passez à l' étape 4 , si les critères d'arrêt sont remplis, terminez et retournez la meilleure solution.


    ###### Étape 4: Mettez à jour la liste Tabu , les critères d'aspiration et passez à l' étape 1

    memoire = []
    posMemoire = 0
    continu = True  # critère d'arrêt : nombre d'itération max autorisé de 1000
    iteration = 0
    while continu:
        solutionTemp = meilleurVoisin(solution, memoire)
        if cout(solutionTemp) < cout(solution):
            if len(memoire) < tailleMemoire:
                memoire.append(solution)
            else:
                memoire[posMemoire] = solution
                posMemoire = (posMemoire+1) % tailleMemoire
        solution = solutionTemp
        iteration += 1
        if iteration > 1000:
            continu = False
    return optimum(memoire)


def meilleurVoisin(solution, memoire):
    # retourne le voisin ayant le meilleur cout parmi l'ensemble des voisins n'étant pas dans mémoire
    return solution


def cout(solution):
    # calcule le cout (et donc l'optimialité) associée à une solution. Un cout arbitrairement élevé est appliqué pour une solution non faisable.
    return "gratuit !- pour l'instant"


def optimum(tableau):
    # retourne la solution ayant le cout le plus intéressant des solutions stockées en mémoire
    min, indMin = -1, -1
    for i in range(len(tableau)):
        if cout(tableau[i]) < min or min == -1:
            min = cout(tableau[i])
            indMin = i
    return tableau[indMin]


def voisinage(solution,D,creneauxDispo):
    """
    Solution est un dictionnaire de la forme :

    Employé1
        Indice de la Tache 1
            Indice de la tache précédente \n
            Indice de la tache suivante \n
            heure de début de la tache \n
        Indice de la Tache 2 
            ...
    Employé2
        ...

    D est la matrice des distance entre les taches
    creneauxDispo[i] est le np.array de crénaux de DISPONIBILITE de la tache i de la forme [[100,400],[500,800]]
    """
    
    




