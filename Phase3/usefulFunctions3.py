import numpy as np


def fonctionRestriction(capacite, X):
    pass


def triOpti(tachesFaisables, localisationCourante, distance, duree):
    '''
    Fonction ayant pour objectif de trier les numéros des taches en fonction de leur optimalité vis-à-vis du critère d'optimisation local choisi
    ENTREES
    - tachesFaisables : liste des indices des taches faisables
    - localisationCourante : indice de la dernière tache effectuée par l'employé (permet de déterminer sa position comme étant celle de la dernière tache effectuée)
    - distance : matrice contenant les distances entre la tache d'indice colonne et la tache d'indice ligne
    SORTIES
    - tableau trié des taches de la plus avantageuse à la moins avantageuse
    '''
    '''
    selon quel critère optimiser ? 
    Choix d'optimiser en fonction de l'argent gagné = cout horaire du dépanage*duree-cout transport*distance
    '''
    # création d'une liste contenant les valeurs de cout associées à la tache
    cout = np.zerros(len(tachesFaisables))
    for i in range(len(tachesFaisables)):
        cout[i] = 2/3*duree+(12/0.833-(0.575+0.12)) * \
            distance(tachesFaisables[i], localisationCourante)
    tachesFaisables = np.array(tachesFaisables)
    inds = cout.argsort()
    return tachesFaisables[inds]


def tachesRealisable(tacheOpti, duree, debut, fin, finJourneeEmploye, indispoDico):
    '''
    fonction qui vérifie qu'au moins une tâche est réalisable par l'employé avant la fin de la journée, qui retourne :
    - raison valant 'indisponibilité', si une indisponibilité bloque la réalisation d'une de ces tâches, 'fin de journée'-temps de transport pour rentrer chez soi si aucun tâche n'est faisable avant la fin de journée, 'déjeuner' si le déjeuner bloque, none sinon
    - tache : le numéro de la tache optimale faisable, si une tache au moins est faisable, none sinon
    '''
    # comment prendre en compte les ouvertures et les fermetures ?
    # heureButtoire = min(heure de fin, heure d'indispo - si existe-, Hfin de pause dej-temps de dej si pause non faite)

    pass
