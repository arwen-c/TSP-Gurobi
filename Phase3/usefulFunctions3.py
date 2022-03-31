from msilib.schema import Error
import numpy as np
from sympy import solve


def estDansUnCrenaux(heure,crenaux):
    n = len(crenaux)
    for j in range(n):
        print(crenaux[j])
        print(heure)
        if crenaux[j][0] <= heure <= crenaux[j][1] :
            return True
        elif j < n-1 and crenaux[j][1] <= heure <= crenaux[j+1][0]:
            return crenaux[j+1][0] 
    return "Error"

def MAJHeureDebut(i0,solution_k,crenauxDispo_k,Duree,D):

    iCourant = i0
    suivantCourant = solution_k[i0]["suivant"]

    while suivantCourant != 0: # tant qu'on arrive pas à la maison

        precedentCourant = solution_k[iCourant]["precedent"]
        suivantCourant = solution_k[iCourant]["suivant"]

        h = solution_k[precedentCourant]["heure"] + Duree[precedentCourant] + D[precedentCourant,iCourant]/0.833
        print(iCourant)
        if estDansUnCrenaux(h,crenauxDispo_k[iCourant]) == "Error":
            
            return "Error"
        elif estDansUnCrenaux(h,crenauxDispo_k[iCourant]) == True:
            solution_k[iCourant]["heure"] = int(h)
        elif h + Duree[iCourant] + D[iCourant,0]/0.833 <= 18*60 : # heure de fin des employés
            solution_k[iCourant]["heure"] = estDansUnCrenaux(h,crenauxDispo_k[iCourant])
        else : 
            solution_k[iCourant] = solution_k[0]
            return solution_k

        iCourant = suivantCourant

    return solution_k

# sol_test = {0:{"precedent" : None, "suivant" : 3, "heure": 8*60}, 1:{"precedent" : 3, "suivant" : 2}, 2:{"precedent" : 1, "suivant" : 0}, 3:{"precedent" : 0, "suivant" : 1}}
# crenauxDispo_test = 60*np.array([np.array([[8,11],[13,18]]),np.array([[8,12],[12,17]]),np.array([[8,18]]),np.array([[8,10],[14,16],[17,18]])])
# Duree = 30*np.ones((5,1))
# D = np.array([[0, 2, 5, 1],
#               [2, 0, 4, 3],
#               [5, 4, 0, 6],
#               [1, 3, 6, 0]])
# i0 = 3

# print(MAJHeureDebut(i0,sol_test,crenauxDispo_test,Duree,D))
