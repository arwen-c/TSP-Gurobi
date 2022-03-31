from cmath import inf
from msilib.schema import Error
import numpy as np
from sympy import solve


def estDansUnCreneau(heure,creneau):
    n = len(creneau)
    for j in range(n):
        if creneau[j][0] <= heure <= creneau[j][1] :
            return True
    return False

def getCreneaux(heure,creneauxTache):
    """Cette fonction renvoie l'heure de début et l'heure de fin du crénaux de disponibilité contenant l'heure donnée"""
    n = len(creneauxTache)
    for j in range(n):
        if creneauxTache[j][0] <= heure <= creneauxTache[j][1] :
            return creneauxTache[j][0], creneauxTache[j][1]

def MAJTempsSuivants(i0,solution_k,creneauxDispo_k,Duree,D):
    """Cette fonction permet de contracter les temps en aval d'une tache i0. Autrement dit elle tasse les heures en fin de journée à partir d'une tache i0 incluse"""

    iCourant = 0
    precedentCourant = solution_k[iCourant]["precedent"]
    h = int(18*60 - D[precedentCourant,iCourant]/0.833)

    while iCourant != i0 : # tant qu'on arrive pas à la maison

        # On regarde si la tache d'après peut être faite avant l'heure prévu tout en restant dans le crénaux de dispo
        hmin,hmax = getCreneaux(solution_k[precedentCourant]["heure"],creneauxDispo_k[precedentCourant])

        if hmin + Duree[precedentCourant] <= h <= hmax :
            solution_k[precedentCourant]["heure"] = int(h - Duree[precedentCourant])

        elif h > hmax :
            solution_k[precedentCourant]["heure"] = int(hmax - Duree[precedentCourant])

        else:
            print("Error") 

        iCourant = precedentCourant
        precedentCourant = solution_k[iCourant]["precedent"]
        h = int(solution_k[iCourant]["heure"] - D[precedentCourant,iCourant]/0.833)

    return solution_k

        

def MAJTempsPrecedents(i0,solution_k,creneauxDispo_k,Duree,D):
    """Cette fonction permet de contracter les temps en amont d'une tache i0. Autrement dit elle tasse les heures en début de journée à partir d'une tache i0 incluse"""

    iCourant = 0
    suivantCourant = solution_k[iCourant]["suivant"]


    while iCourant != i0: # tant qu'on arrive pas à la maison

        # On regarde si la tache d'après peut être faite avant l'heure prévu tout en restant dans le crénaux de dispo
        h = int(solution_k[iCourant]["heure"] + Duree[iCourant] + D[iCourant,suivantCourant]/0.833)
        hmin,hmax = getCreneaux(solution_k[suivantCourant]["heure"],creneauxDispo_k[suivantCourant])

        if hmin <= h <= hmax :
            solution_k[suivantCourant]["heure"] = h

        elif h < hmin :
            solution_k[suivantCourant]["heure"] = h

        else:
            print("Error") 

        iCourant = suivantCourant
        suivantCourant = solution_k[iCourant]["suivant"]

    return solution_k



# sol_test = {0:{"precedent" : 2, "suivant" : 3, "heure": 8*60}, 1:{"precedent" : 3, "suivant" : 2, "heure" : 11*60}, 2:{"precedent" : 1, "suivant" : 0, "heure" : 14*60}, 3:{"precedent" : 0, "suivant" : 1, "heure" : 10*60}}
# creneauxDispo_k = [[[8*60,18*60]], [[60*8,60*18]], [[60*8,60*12],[60*12,60*17]], [[60*8,60*18]], [[60*8,60*10],[60*14,60*16],[60*17,60*18]]]
# Duree = 30*np.ones((5,1))
# D = np.array([[0, 2, 5, 1, 10],
#               [2, 0, 4, 3, 6],
#               [5, 4, 0, 6, 8],
#               [1, 3, 6, 0, 11],
#               [12, 3, 7, 8, 0]])
# i0 = 1
# tGlande = np.NaN*np.zeros((4,4))
# print(MAJTempsSuivants(2,MAJTempsPrecedents(i0,sol_test,creneauxDispo_k)[0],creneauxDispo_k))


# pour prendre en compte la pause dej en mettant une indispo employé à lieu non fixé none
