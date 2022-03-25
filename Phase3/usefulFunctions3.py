from Phase2.usefulFunctions2 import recuperationHeure
import math


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


def triOpti(tachesFaisables, localisationCourante, distance, tachesDico):
    '''
    Fonction ayant pour objectif de trier les numéros des taches en fonction de leur optimalité vis-à-vis du critère d'optimisation local choisit :
    - tachesFaisables : liste des indices des taches faisables
    - localisationCourante : indice de la dernière tache effectuée par l'employé (permet de déterminer sa position comme étant celle de la dernière tache effectuée)
    - distance : matrice contenant les distances entre la tache d'indice colonne et la tache d'indice ligne
    '''
    listeOpti = []
    nbreTachesFaisables = len(tachesFaisables)
    for k in range(nbreTachesFaisables):
        coutTache = distance(localisationCourante, k)/0.833 - \
            tachesDico[tachesFaisables[k]]['TaskDuration']
        # creation de la liste par tri de la liste par insertion
    return listeOpti


def tachesRealisable(tacheOpti, duree, debut, fin, finJourneeEmploye, indispoDicoEmployeN, t, pauseFaite, localisationCourante, distance, tachesDico):
    '''
    tacheOpti = liste des tâches triées selon l'optimisation de l'objectif ;
    duree = vecteur durée des tâches ;
    debut = vecteur avec les ouvertures des tâches après chaque indisponibilité ;
    fin = vecteur avec les ouvertures des tâches avant chaque indisponibilité ;
    finJourneeEmploye = heure de fin de la journée de l'employé sélectionné ;
    indispoDico = dictionnaire qui regroupe les informations relatives aux indisponibilités de l'emplyé sélectionné.

    Cette fonction vérifie qu'au moins une tâche est réalisable par l'employé avant la fin de la journée, qui retourne :
    - raison valant 'indisponibilité', si une indisponibilité bloque la réalisation d'une de ces tâches, 'fin de journée' si aucun tâche n'est faisable avant la fin de journée, 'déjeuner' si le déjeuner bloque, none sinon
    - tache : le numéro de la tache optimale faisable, si une tache au moins est faisable, none sinon
    '''
    # comment prendre en compte les ouvertures et les fermetures ?
    # heureButtoire = min(heure de fin, heure d'indispo - si existe-, Hfin de pause dej-temps de dej si pause non faite)

    raison = ''
    tache = None
    tacheOptiFaisableTrouvee = False
    m = len(tacheOpti)
    k = 0
    while not(tacheOptiFaisableTrouvee) and k < m:
        if finJourneeEmploye > t + distance(localisationCourante, tacheOpti[k])/0.833 + duree[tacheOpti[k]] + distance(tacheOpti[k], k)/0.833:
            nbreCreneauxDebutK = len(debut[k])
            creneauConvenable = False
            c = 0
            while not(creneauConvenable) and c < nbreCreneauxDebutK:
                # + 10: # le +10 peermet de ne pas rater une tache optimale à quelques minutes près 10 en l'occurence ici
                if t + distance(localisationCourante, tacheOpti[k])/0.833 > debut[k][c]:
                    # + 10 en fait pb il faudrait savoir si on a bien rajouté ces 10 min boucle while  # on regarde la fin de créneau correspondante + il faut faire attention au décalage qu'on a pu créer précédemment avec le + 10
                    if t + distance(localisationCourante, tacheOpti[k])/0.833 + duree[k] < fin[k][c]:
                        creneauConvenable = True
                c += 1
            pasIndispo = False
            if creneauConvenable:
                deltaLong = tachesDico[localisationCourante]['Longitude'] - \
                    indispoDicoEmployeN['Longitude']
                deltaLat = tachesDico[localisationCourante]['Latitude'] - \
                    indispoDicoEmployeN['Latitude']
                distancePourIndispo = (
                    1.852*60*math.sqrt(deltaLong**2 + deltaLat**2))
                pasIndispo = recuperationHeure(indispoDicoEmployeN['Start']) < t + distance(
                    localisationCourante, tacheOpti[k])/0.833 + duree[k] + distancePourIndispo/0.833
                if not(pasIndispo):  # si on a bien une indisponibilité
                    raison = 'indisponibilité'
            if creneauConvenable and pasIndispo:
                if t < 720:
                    if t + distance(localisationCourante, tacheOpti[k])/0.833 + duree[tacheOpti[k]] < 780:
                        tache = tacheOpti[k]
                elif t > 840:
                    tache = tacheOpti[k]
                else:
                    if pauseFaite:
                        tache = tacheOpti[k]
                    else:
                        raison = 'déjeuner'
        else:
            raison = 'fin de journée'
        k += 1
    return raison, tache
