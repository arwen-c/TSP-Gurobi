

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


def triOpti(tachesFaisables, localisationCourante, distance):

    pass


def tachesRealisable(tacheOpti, duree, debut, fin, finJournéeEmploye, indispoDico):
    '''
    fonction qui vérifie qu'au moins une tâche est réalisable par l'employé avant la fin de la journée, qui retourne :
    - raison valant 'indisponibilité', si une indisponibilité bloque la réalisation d'une de ces tâches, 'fin de journée' si aucun tâche n'est faisable avant la fin de journée, 'déjeuner' si le déjeuner bloque, none sinon
    - tache : le numéro de la tache optimale faisable, si une tache au moins est faisable, none sinon
    '''
    # heureButtoire = min(heure de fin, heure d'indispo - si existe-, Hfin de pause dej-temps de dej si pause non faite)

    pass
