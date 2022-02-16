# importations de module
import numpy as np
import matplotlib.pyplot as plt
from gurobipy import *

# variables dont on hérite des programmes précédents
# cni
# nbre_employe numéroté de 0 à n-1
# nbre_taches
# D : tableau contenant la distance entre les tâches i et j en position (i,j)


def optimisation_1(cni, nbre_employe, nbre_taches, D):

    m = Model("Modele exact simple")
    # ajout variables de décisions
    # temps à laquelle commencent les tâches
    H = m.addVar(shape=nbre_employe, lb=0)
    X = np.array(
        m.addVar(shape=(nbre_employe, nbre_taches, nbre_taches), lb=0, ub=1))

    # -- Ajout des constraintes --
    m.addConstr(sum(X[n, i, j]) <= -5, name="C1")
    # m.addConstr( <= 10, name = "C2")

    # -- Ajout de la fonction objectif. Produit terme à terme
    X_inter = sum(X[n]*np.array(D) for n in range(nbre_employe))
    m.setObjective(sum(X_inter[i, j]
                       for i, j in range(nbre_taches)), GRB.MINIMIZE)

    m.update()  # Mise à jour du modèle
    m.optimize()  # Résolution

    # -- Affichage des solutions --
    print("Les solutions optimales sont")
    print("X =", X.x)
    print("avec pour valeur de l'objectif z =", m.objVal)
    return m.objVal
