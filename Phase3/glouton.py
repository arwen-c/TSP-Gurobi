from matplotlib.cbook import safe_masked_invalid
import numpy as np
from sympy import E

# qu'est ce que dicoTachesEtendues ?


def optiGloutonSansRepas(capacite, distance, duree, debut, fin, nbreTaches, employeesDico, indispoDico):
    """Variables dont on hérite des programmes précédents :
    capacite = matrice des capacité de l'ouvrier n à faire la tache i ;
    distance = matrice contenant la distance entre les tâches i et j en position (i,j) ;
    duree = liste des durées des tâches ;
    debut = liste des horaires de début des tâches ;
    fin = liste des horaires de fin des tâches ;
    employeesDico = liste de dictionnaire contenant pour chaque employé un dictionnaire de ses caractéristiques
    indispoDico = dictionnaire de dictionnaire contenant en clef le nom de la personne, et en argument un dictionnaire des caractéristiques"""
    # on peut modifier le programme pour se passer de employeesDico
    nombreEmploye = len(employeesDico)
    nombreTachesTotal = len(employeesDico+indispoDico)
    # vaut 1 si la tâche i est fait par l'employé n
    X = np.zeros(nombreEmploye, nombreTachesTotal, nombreTachesTotal)
    # heures de début des pauses dèj
    L = np.zeros(nombreEmploye, nombreTachesTotal, nombreTachesTotal)
    H = np.zeros(nombreTachesTotal)  # heure de début de chaque tâche
    tempsTravail = 0
    distanceParcourue = 0
    for n in range(nombreEmploye):
        employe = employeesDico[n]
        t = employe['StartTime']
        # numéro de la tâche à laquelle on est, ici tache fictive du départ
        localisationCourante = nbreTaches+n
        newTachePossible = True
        # contrainte compétence, on obtient une liste de tâches auxquelles on enlève les tâches qui ont déjà été faites et celles que l'employé n'est pas capable de faire
        # créé une liste des numéros des tâches restantes
        tachesFaisables = fonctionRestriction(capacite, X)
        while newTachePossible:  # on construit la journée d'un employé au fur et à mesure
            # pb à résoudre : prise en compte des pauses méridiennes
            # on regarde toutes les tâches possibles, et on les classes dans l'ordre des plus optimales en terme de temps + distance à la position actuelle
            tacheOpti = triOpti(
                tachesFaisables, localisationCourante, distance)
            # on vérifie qu'au moins une des tâches peut se faire sans empiéter sur une periode d'indisponibilité, dans la periode d'ouverture de la tache et de disponibilité de l'employé
            tache, raison = tachesRealisable(
                tacheOpti, duree, debut, fin, employe['EndTime'], indispoDico, t, True)  # rôle à bien définir
            if tache == None:
                if raison == 'indisponibilité':
                    t = indispoDico[employe['EmployeeName']]['End']
                if raison == 'fin de journée':
                    newTachePossible = False
            # si au moins une des tâches est faisable
            else:
                X[n, tache] = 1
                H[tache] = max(debut[tache], t+distance[tache]/0.833)
                t = H[tache]+duree[tache]
                tempsTravail += duree[tache]
                distanceParcourue += distance[tache, localisationCourante]
                localisationCourante = tache
    return X, H, L, distanceParcourue, tempsTravail

# idée de l'algo : on regarde ce qui maximise un critère (-temps de transport + durée de travail), on regarde si la tache est ouverte, si oui on la fait
# Sinon on compare avec les taches suivantes jusqu'a trouver une tâche ouverte


def optiGlouton(capacite, distance, duree, debut, fin, nbreTaches, employeesDico, indispoDico):
    """Variables dont on hérite des programmes précédents :
    capacite = matrice des capacité de l'ouvrier n à faire la tache i ;
    distance = matrice contenant la distance entre les tâches i et j en position (i,j) ;
    duree = liste des durées des tâches ;
    debut = liste des horaires de début des tâches ;
    fin = liste des horaires de fin des tâches ;
    employeesDico = liste de dictionnaire contenant pour chaque employé un dictionnaire de ses caractéristiques
    indispoDico = dictionnaire de dictionnaire contenant en clef le nom de la personne, et en argument un dictionnaire des caractéristiques"""
    # on peut modifier le programme pour se passer de employeesDico
    nombreEmploye = len(employeesDico)
    # vaut 1 si la tâche i est fait par l'employé n
    X = np.zeros(nombreEmploye, nbreTaches, nbreTaches)
    L = np.zeros(nombreEmploye)  # heures de début des pauses dèj
    H = np.zeros(nbreTaches)  # heure de début de chaque tâche
    tempsTravail = 0
    distanceParcourue = 0
    for n in range(nombreEmploye):
        employe = employeesDico[n]
        t = employe['StartTime']
        # numéro de la tâche à laquelle on est, ici tache fictive du départ
        localisationCourante = nbreTaches+n
        pauseFaite = False
        newTachePossible = True
        # contrainte compétence, on obtient une liste de tâches auxquelles on enlève les tâches qui ont déjà été faites et celles que l'employé n'est pas capable de faire
        # créé une liste des numéros des tâches restantes
        tachesFaisables = fonctionRestriction(capacite[n, :], X)
        while newTachePossible:  # on construit la journée d'un employé au fur et à mesure
            # on regarde toutes les tâches possibles, et on les classes dans l'ordre des plus optimales en terme de temps + distance à la position actuelle
            tacheOpti = triOpti(
                tachesFaisables, localisationCourante, distance)
            # on vérifie qu'au moins une des tâches peut se faire sans empiéter sur une periode d'indisponibilité, sur la pause repas, dans la periode d'ouverture de la tache et de disponibilité de l'employé
            tache, raison = tachesRealisable(
                tacheOpti, duree, debut, fin, employe['EndTime'], indispoDico, t, pauseFaite)  # rôle à bien définir
            if tache == None:
                if raison == 'indisponibilité':
                    t = indispoDico[employe['EmployeeName']]['End']
                if raison == 'fin de journée':
                    newTachePossible = False
                if raison == 'déjeuner':
                    L[n] = t
                    t += 60
                    pauseFaite = True
            # si au moins une des tâches est faisable
            else:
                X[n, tache] = 1
                H[tache] = max(debut[tache], t+distance[tache]/0.833)
                t = H[tache]+duree[tache]
                tempsTravail += duree[tache]
                distanceParcourue += distance[tache, localisationCourante]
                localisationCourante = tache
    return X, H, L, distanceParcourue, tempsTravail


'''
Boucle proposée par SamDa

while t < finJourneeEmploye:  # on construit la journée d'un employé au fur et à mesure
            # on regarde les tâches ouvertes au temps t ou qui vont s'ouvrir
            listeTachesPossibles = fonctionTachesPossibles(
                t, localisationCourante, matDistance, vecDuree, vecDebut, vecFin, employe, tachesFaisables) #ensemble des fonctions qui seront ouvertes le tempds d'y arriver (à voir, pourrait être plus intéressant d'attendre un peu l'ouverture - quand prendre en compte le temps ?)
                # mettre la pause dèj dans les indisponibilités
                # liste ordonnée, la première tâche est la plus proche et la plus longue en durée (trouver un critère qui permet d'optimiser les 2)
# vérifier que l'employé n'est pas en pause, qu'il n'est pas en indisponibilité et qu'il peut faire sa pause dèj
            nombreTachesPossibles = len(listeTachesPossibles)
            if nombreTachesPossibles > 0:
                prochaineTacheTrouvee = False
                i = 0
                while not(prochaineTacheTrouvee) and i < nombreTachesPossibles:
                    prochaineTacheTrouvee, idTache = verificationContrainteIndisponibilites(
                        dicoIndis, listeTachesPossibles[i])
                if prochaineTacheTrouvee:
                    t += vecDuree[idTache]
                    X[n, idTachePrecedente, idTache] = #idTacheprecedente à trouver
                elif not(pauseFaite) and t < 840:
                    pauseFaite = True
                    t += 45 #
                elif

'''
