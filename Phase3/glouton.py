# from matplotlib.cbook import safe_masked_invalid
# from asyncio import ThreadedChildWatcher
from sys import displayhook
import numpy as np
from sympy import E
from usefulFunctions3 import *

# qu'est ce que dicoTachesEtendues ?


# def optiGloutonSansRepas(capacite, distance, duree, debut, fin, nbreTaches, employeesDico, indispoDico):
#     """Variables dont on hérite des programmes précédents :
#     capacite = matrice des capacité de l'ouvrier n à faire la tache i ;
#     distance = matrice contenant la distance entre les tâches i et j en position (i,j) ;
#     duree = liste des durées des tâches ;
#     debut = liste des horaires de début des tâches ;
#     fin = liste des horaires de fin des tâches ;
#     employeesDico = liste de dictionnaire contenant pour chaque employé un dictionnaire de ses caractéristiques
#     indispoDico = dictionnaire de dictionnaire contenant en clef le nom de la personne, et en argument un dictionnaire des caractéristiques"""
#     # on peut modifier le programme pour se passer de employeesDico
#     nombreEmploye = len(employeesDico)
#     nombreTachesTotal = len(employeesDico+indispoDico)
#     # vaut 1 si la tâche i est fait par l'employé n
#     X = np.zeros(nombreEmploye, nombreTachesTotal, nombreTachesTotal)
#     # heures de début des pauses dèj
#     L = np.zeros(nombreEmploye, nombreTachesTotal, nombreTachesTotal)
#     H = np.zeros(nombreTachesTotal)  # heure de début de chaque tâche
#     tempsTravail = 0
#     distanceParcourue = 0
#     for n in range(nombreEmploye):
#         employe = employeesDico[n]
#         t = employe['StartTime']
#         # numéro de la tâche à laquelle on est, ici tache fictive du départ
#         localisationCourante = nbreTaches+n
#         newTachePossible = True
#         # contrainte compétence, on obtient une liste de tâches auxquelles on enlève les tâches qui ont déjà été faites et celles que l'employé n'est pas capable de faire
#         # créé une liste des numéros des tâches restantes
#         tachesFaisables = fonctionRestriction(capacite, X)
#         while newTachePossible:  # on construit la journée d'un employé au fur et à mesure
#             # pb à résoudre : prise en compte des pauses méridiennes
#             # on regarde toutes les tâches possibles, et on les classes dans l'ordre des plus optimales en terme de temps + distance à la position actuelle
#             tachesOpti = triOpti(
#                 tachesFaisables, localisationCourante, distance)
#             # on vérifie qu'au moins une des tâches peut se faire sans empiéter sur une periode d'indisponibilité, dans la periode d'ouverture de la tache et de disponibilité de l'employé
#             tache, raison = tachesRealisables(
#                 tachesOpti, duree, debut, fin, employe['EndTime'], indispoDico, t, True)  # rôle à bien définir
#             if tache == None:
#                 if raison == 'indisponibilité':
#                     t = indispoDico[employe['EmployeeName']]['End']
#                 if raison == 'fin de journée':
#                     newTachePossible = False
#             # si au moins une des tâches est faisable
#             else:
#                 X[n, tache] = 1
#                 H[tache] = max(debut[tache], t+distance[tache]/0.833)
#                 t = H[tache]+duree[tache]
#                 tempsTravail += duree[tache]
#                 distanceParcourue += distance[tache, localisationCourante]
#                 localisationCourante = tache
#     return X, H, L, distanceParcourue, tempsTravail

# idée de l'algo : on regarde ce qui maximise un critère (-temps de transport + durée de travail), on regarde si la tache est ouverte, si oui on la fait
# Sinon on compare avec les taches suivantes jusqu'a trouver une tâche ouverte


def optiGlouton(capacite, distance, duree, debut, fin, nbreTaches, employeesDico, indispoDico, tachesDico):
    """Variables dont on hérite des programmes précédents :
    capacite = matrice des capacité de l'ouvrier n à faire la tache i ;
    distance = matrice contenant la distance entre les tâches i et j en position (i,j) ;
    duree = liste des durées des tâches ;
    debut = liste des horaires de début des tâches ;
    fin = liste des horaires de fin des tâches ;
    employeesDico = liste de dictionnaire contenant pour chaque employé un dictionnaire de ses caractéristiques
    indispoDico = liste de dictionnaire où le dictionnaire n a les caractéristiques des indispo de l'employé n"""
    # on peut modifier le programme pour se passer de employeesDico
    nombreEmploye = len(employeesDico)
    # vaut 1 si la tâche i est fait par l'employé n
    # on change la taille des données pour simplifier normalement X = np.zeros((nombreEmploye, nbreTaches, nbreTaches)), modification dans usefulFunctions3 : fonctionRestrcition et lignesSolution
    X = np.zeros((nombreEmploye, nbreTaches))
    L = np.zeros(nombreEmploye)  # heures de début des pauses dèj
    H = np.zeros(nbreTaches)  # heure de début de chaque tâche
    tempsTravail = 0
    distanceParcourue = 0
    for n in range(nombreEmploye):
        employe = employeesDico[n]
        t = recuperationHeure(employe['WorkingStartTime'])
        # numéro de la tâche à laquelle on est, ici tache fictive du départ
        localisationCourante = nbreTaches + n
        pauseFaite = False
        newTachePossible = True
        # contrainte compétence, on obtient une liste de tâches auxquelles on enlève les tâches qui ont déjà été faites et celles que l'employé n'est pas capable de faire
        # créé une liste des numéros des tâches restantes
        vecCapaciteEmployeN = capacite[n, :]
        tachesFaisables = fonctionRestriction(vecCapaciteEmployeN, X)
        # si on ne change pas la taille de X (voir plus haut) pour rester cohérent avec le modèle précédent on doit ajouter une variable tachePrecedente
        indispoDicoEmployeN = {}
        k = 0
        while k < len(indispoDico):
            if indispoDico[k]['EmployeeName'] == employe['EmployeeName']:
                indispoDicoEmployeN = indispoDico[k]
                # permet l'arrêt de la boucle une fois l'indisponibilité trouvée
                k = len(indispoDico)
            k += 1
        while newTachePossible:  # on construit la journée d'un employé au fur et à mesure
            # on regarde toutes les tâches possibles, et on les classes dans l'ordre des plus optimales en terme de temps + distance à la position actuelle
            tachesOpti = triOpti(
                tachesFaisables, localisationCourante, distance, duree)
            # on vérifie qu'au moins une des tâches peut se faire sans empiéter sur une periode d'indisponibilité, sur la pause repas, dans la periode d'ouverture de la tache et de disponibilité de l'employé
            raison, tache, creneau = tachesRealisables(
                tachesOpti, duree, debut, fin, recuperationHeure(employe['WorkingEndTime']), indispoDicoEmployeN, t, pauseFaite, localisationCourante, distance, tachesDico, n, nbreTaches)  # rôle à bien définir
            print(raison)
            print(tache)
            print(employe['EmployeeName'])
            if tache == None:
                if raison == 'indisponibilité':
                    t = recuperationHeure(
                        indispoDico[n]['End'])
                if raison == 'fin de journée':
                    newTachePossible = False
                if raison == 'déjeuner':
                    L[n] = max(t, 720)
                    t += L[n] + 60
                    pauseFaite = True
            # si au moins une des tâches est faisable
            else:
                X[n, tache] = 1
                H[tache] = max(debut[tache][creneau - 1], t +
                               distance[localisationCourante][tache]/0.833)  # on utilise bien le créneau c-1, en effet on ajoute 1 au créneau convenable dans la boucle de la fonction tachesRealisables
                t = H[tache] + duree[tache]
                tempsTravail += duree[tache]
                distanceParcourue += distance[tache][localisationCourante]
                localisationCourante = tache
                # on enlève la tache que l'on vient de faire du tableau des possibilités
                i = 0
                aTrouve = True
                while i < len(tachesFaisables) and aTrouve:
                    if tachesFaisables[i] == tache:
                        tachesFaisables.pop(i)
                        aTrouve = False
                    i += 1
    return [X, H, L, distanceParcourue, tempsTravail]


# tant que encore tache
# faire pour tout employe dispo (boucle for)
# regarder score et le sauvegarder
# comparer les scores et prendre le meilleur

# hyp pause dej à l'endroit de la dernière tâche possible => on réduit l'ensemble des solutions
