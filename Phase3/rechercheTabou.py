from distutils.log import ERROR
from re import M
from glouton import *
import numpy as np
from usefulFunctions3 import * 

# question : comment caractériser une solution ? Par la matrice des X ? Ca rend la comparaison entre plusieurs solutions assez laborieuse pour de grandes instances
# quel critère d'arrêt ? pour une première version, utilisation d'un nombre d'itération maximum. Par la suite, on peut améliorer le programme en utilisant un nombre max d'itération depuis la dernière mise à jour d'un minimum (dernier ajout à la liste tabou)
# d'autres améliorations, notamment sur la tailleMemoire sont proposées dans le poly de métaheuristique


def rechercheTabou(capacite, matDistance, duree, debut, fin, nbreTaches, employeesDico, indispoDico, tachesDico, tailleMemoire):
    solution = optiGlouton(capacite, matDistance, duree, debut,
                           fin, nbreTaches, employeesDico, indispoDico, tachesDico)
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
    
    

def insertionTache(i,precedent,suivant,solution_k,creneauxDispo_k,Duree,D):
    """solution_k designe le graph de l'employé k idem pour creneauxDispo_k"""

    ###### 1ere étape : tasser à gauche et à droite les heures pour maximiser le succès de l'insertion

    solution_k = MAJTempsPrecedents(precedent,solution_k,creneauxDispo_k,Duree,D)
    solution_k = MAJTempsSuivants(suivant,solution_k,creneauxDispo_k,Duree,D)

    ###### 2eme étape : inserer

    solution_k[precedent]["suivant"] = i
    solution_k[suivant]["precedent"] = i
    solution_k[i] = {"precedent":precedent,"suivant":suivant}
    
    if estDansUnCreneau(solution_k[precedent]["heure"] + Duree[precedent] + D[precedent,i]/0.833,creneauxDispo_k[i]):
        solution_k[i]["heure"] = int(solution_k[precedent]["heure"] + Duree[precedent] + D[precedent,i]/0.833)

    else:
        debuts = [creneauxDispo_k[i][j][0] for j in range (len(creneauxDispo_k[i]))].sort()
        found = 0
        for hmin in debuts:
            if hmin > solution_k[precedent]["heure"] + Duree[precedent] + D[precedent,i]/0.833 and found == 0:
                solution_k[i]["heure"] = hmin
                found = 1 

    ####### 3eme étape : vérifier que la solution est faisable au niveau des indisponibilité des taches

    if solution_k[i]["heure"] + Duree[i] + D[i,suivant]/0.833 > solution_k[suivant]["heure"]:
        print("insertion impossible")
        return None
            
    return solution_k

def suppressionTache(i,solution_k,creneauxDispo_k,Duree,D):
    precedent = solution_k[i]["precedent"]
    suivant = solution_k[i]["suivant"]
    solution_k[precedent]["suivant"] = suivant
    solution_k[suivant]["precedent"] = precedent
    del solution_k[i]

    return solution_k


sol_test = {0:{"precedent" : 2, "suivant" : 3, "heure": 8*60}, 1:{"precedent" : 3, "suivant" : 2, "heure" : 8.5*60}, 2:{"precedent" : 1, "suivant" : 0, "heure" : 11*60}, 3:{"precedent" : 0, "suivant" : 1, "heure" : 10*60}}

# attention je ne dois pas prendre en compte la pause dej dans maj heuee

creneauxDispo_test = [[[8*60,12*60],[13*60,18*60]]]*5
Duree = 30*np.ones((5,1))
D = np.array([[0, 2, 5, 1, 10],
              [2, 0, 4, 3, 6],
              [5, 4, 0, 6, 8],
              [1, 3, 6, 0, 11],
              [12, 3, 7, 8, 0]])
i0 = 3
tGlande = np.NaN*np.zeros((4,4))


print(insertionTache(4,3,1,sol_test,creneauxDispo_test,Duree,D))
print(suppressionTache(1,sol_test,creneauxDispo_test,Duree,D))