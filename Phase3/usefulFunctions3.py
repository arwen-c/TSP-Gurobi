import numpy as np


def fonctionRestriction(capaciteEmploye, X):
    """capaciteEmploye = matrice des compétences
    X = matrice d'affectation des tâches, l'employé n va de la tâche i à la tâche j
    Cette fonction permet de restreindre la recherche de taches que l'employé va faire en vérifiant la contrainte de compétences et si la tâche a déjà été faite.
    Renvoie une liste d'identifiant de tâches.
    """
    listeTaches = []
    nbreTache = capaciteEmploye.shape
    nbreEmploye, _, _ = X.shape
    for k in range(nbreTache):
        if capaciteEmploye[k] == 1:
            tacheNonFaite = True
            n = 0
            while tacheNonFaite and n < nbreEmploye:
                i = 0
                while tacheNonFaite and i < nbreTache:
                    if X[n, i, k] == 1:  # or X[n, k, i] == 1: normalement pas besoin de regarder dans les 2 sens
                        tacheNonFaite = False
                    i += 1
                n += 1
            if tacheNonFaite:
                listeTaches.append(k)
    # peut-être renvoyer une liste de dictionnaires pour travailler avec une instance plus petite dans la fonction glouton et donc gagner en complexité (mais peut-être inutile)
    return listeTaches


def triOpti(tachesFaisables, localisationCourante, distance, duree):
    # création d'une liste contenant les valeurs de cout associées à la tache
    cout = np.zerros(len(tachesFaisables))
    for i in range(len(tachesFaisables)):
        cout[i] = 2/3*duree+(12/0.833-(0.575+0.12)) * \
            distance(tachesFaisables[i], localisationCourante)
    tachesFaisables = np.array(tachesFaisables)
    inds = cout.argsort()
    return tachesFaisables[inds]


def tachesRealisable(tacheOpti, duree, distance, localisationCourante, debut, fin, finJournéeEmploye, indispoDico):
    '''
    Fonction ayant pour objectif de trier les numéros des taches en fonction de leur optimalité vis-à-vis du critère d'optimisation local choisi
    ENTREES
    - tachesFaisables : liste des indices des taches faisables
    - localisationCourante : indice de la dernière tache effectuée par l'employé (permet de déterminer sa position comme étant celle de la dernière tache effectuée)
    - distance : matrice contenant les distances entre la tache d'indice colonne et la tache d'indice ligne
    SORTIES
    - tableau trié des taches de la plus avantageuse à la moins avantageuse
    selon quel critère optimiser ?
    Choix d'optimiser en fonction de l'argent gagné = cout horaire du dépanage*duree-cout transport*distance
    '''
