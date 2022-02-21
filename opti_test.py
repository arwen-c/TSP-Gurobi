# importations de module
from msilib.schema import Binary
from matplotlib.quiver import QuiverKey
import numpy as np
import matplotlib.pyplot as plt
from gurobipy import *
from pandas import array
from sympy import quadratic_congruence

# variables dont on hérite des programmes précédents
# cni
# nbre_employe numéroté de 0 à n-1
# nbre_taches
# D : tableau contenant la distance entre les tâches i et j en position (i,j)


def optimisation_1(C, nbre_employe, nbre_taches, D, Duree, Debut, Fin):

    m = Model("Modele exact simple")
    # ajout variables de décisions
    # temps à laquelle commencent les tâches
    M = 1440  # majorant des temps
    H = m.addMVar(shape=nbre_taches, lb=0)
    Y = m.addMVar(shape=(nbre_employe, nbre_taches, nbre_taches), lb=0)
    # X = m.addMVar(shape=(nbre_employe, nbre_taches,
    #                      nbre_taches), vtype=GRB.CONTINUOUS, lb=0, ub=1)
    X = m.addMVar(shape=(nbre_employe, nbre_taches,
                         nbre_taches), vtype=GRB.BINARY)

    # modification des types des variables d'entrées pour s'assurer qu'elles conviennent
    C = np.array(C)
    D = np.array(D)

    # -- Ajout des constraintes --
    # toute tâche doit avoir un départ et une arrivée

    m.addConstr(sum(X[n, i, j] for n in range(nbre_employe) for i in range(
        nbre_taches) for j in range(nbre_taches)) == nbre_taches)
    # for i in range(nbre_taches):
    #     m.addConstr(sum(X[n, i, j] for n in range(nbre_employe)
    #                     for j in range(nbre_taches)) == 2)
    # for n in range(nbre_employe):
    #     m.addConstr(sum(X[n, i, j] for j in range(nbre_taches)) == 2)

    for i in range(nbre_taches):
        for j in range(nbre_taches):
            for n in range(nbre_employe):
                # l'employé doit être capable d'effectuer les tâches
                m.addConstr(X[n, i, j] <= C[n, i])
                m.addConstr(X[n, i, j] <= C[n, j])
                # la tache sera bien faite dans l'intervalle de temps choisit
                m.addConstr(H[j]+Duree[j] <= Fin[j])
                m.addConstr(H[j] >= Debut[j])
                # la personne n a le temps de faire la tache j à la suite de la tache i
                m.addConstr(Y[n, i, j]+X[n, i, j] *
                            (Duree[i]+D[i, j]/0.83333) <= H[j])  # 0.833 = vitesse des ouvriers en km.min-1 (équivaut à 50km.h-1)
                m.addConstr(Y[n, i, j] <= H[i])
                m.addConstr(Y[n, i, j] <= X[n, i, j]*M)
                m.addConstr(Y[n, i, j] >= H[i]-M*(1-X[n, i, j]))
    for i in range(nbre_taches):
        for n in range(nbre_employe):
            m.addConstr(X[n, i, i] == 0)

    # -- Ajout de la fonction objectif. Produit terme à terme

    m.setObjective(sum(X[n, i, j]*D[i, j] for n in range(nbre_employe)
                       for i in range(nbre_taches) for i in range(nbre_taches)), GRB.MINIMIZE)

    m.update()  # Mise à jour du modèle
    m.optimize()  # Résolution

    # -- Affichage des solutions --
    print("Les solutions optimales sont")
    print("X =", X.x)
    # print("X =", X[0][0].x)
    print("H =", H.x)
    print("avec pour valeur de l'objectif z =", m.objVal)
    return m.objVal


print(optimisation_1([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 2, 3, [
      [0, 1, 5], [1, 0, 10], [5, 10, 0]], [10, 120, 120], [0, 0, 0], [1300, 1300, 1300]))
