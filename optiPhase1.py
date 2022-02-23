# importations de module
import numpy as np
from gurobipy import *


# variables dont on hérite des programmes précédents
# C=capacité de l'ouvrier n à faire la tache i
# nbre_employe numéroté de 0 à n-1
# nbre_taches
# D : tableau contenant la distance entre les tâches i et j en position (i,j)

# insertion des tâches factice avec le point de départ à ajouter
def ajout_domicile(TasksDico, EmployeesDico):
    for row in EmployeesDico:
        # ajout d'une tâche au départ du domicile
        TasksDico.append({'TaskId': 'Depart'+row['EmployeeName'], 'Latitude': row['Latitude'],    'Longitude': row['Longitude'],
                          'TaskDuration': 0, 'Skill': 0, 'OpeningTime': row['WorkingStartTime'], 'ClosingTime': row['WorkingEndTime']})
        # ajout de l'arrivée au domicile
        TasksDico.append({'TaskId': 'Arrivee'+row['EmployeeName'], 'Latitude': row['Latitude'],    'Longitude': row['Longitude'],
                          'TaskDuration': 0, 'Skill': 0, 'OpeningTime': row['WorkingStartTime'], 'ClosingTime': row['WorkingEndTime']})


def optimisation_1(C, nbre_employe, nbre_taches, D, Duree, Debut, Fin):

    m = Model("Modele exact simple")
    # ajout variables de décisions
    # temps à laquelle commencent les tâches
    M = 1440  # majorant des temps
    H = m.addMVar(shape=nbre_taches, lb=0, ub=1440)
    Y = m.addMVar(shape=(nbre_employe, nbre_taches, nbre_taches), lb=0)
    '''#variable qui vaut 1 en position X[n,i,j] si la personne n fait le trajet de i vers j ??? '''
    X = m.addMVar(shape=(nbre_employe, nbre_taches,
                         nbre_taches),  vtype=GRB.BINARY)
    # modification des types des variables d'entrées pour s'assurer qu'elles conviennent
    C = np.array(C)
    D = np.array(D)

    # -- Ajout des constraintes --

    # toute tâche doit avoir un départ et une arrivée
    for i in range(nbre_taches):
        # chaque tache a bien été faite
        m.addConstr(sum(X[n, i, j] for n in range(nbre_employe)
                        for j in range(nbre_taches)) == 2)
        # vérifier que la même personne arrive et parte de l'endroit donné -> modif Amélie

    for i in range(nbre_taches):
        for j in range(i):
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

    # -- Ajout de la fonction objectif. Produit terme à terme

    m.setObjective(sum(X[n, i, j]*D[i, j] for n in range(nbre_employe)
                       for i in range(nbre_taches) for i in range(nbre_taches)), GRB.MINIMIZE)

    m.update()  # Mise à jour du modèle
    m.optimize()  # Résolution

    # -- Affichage des solutions --
    print("Les solutions optimales sont")
    print("X =", X.x)
    print("H =", H.x)
    print("avec pour valeur de l'objectif z =", m.objVal)
    return X.x, H.x, m.objVal


# print(optimisation_1([[1, 1], [1, 1]], 2, 2, [
#      [0, 10], [10, 0]], [10, 120], [0, 0], [1300, 1300]))
