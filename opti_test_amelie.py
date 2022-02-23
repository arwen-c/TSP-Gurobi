# importations de module
import numpy as np
from gurobipy import *


# variables dont on hérite des programmes précédents
# C=capacité de l'ouvrier n à faire la tache i
# nbre_employe numéroté de 0 à n-1
# nbre_taches
# D : tableau contenant la distance entre les tâches i et j en position (i,j)

# Modification des données pour insérer le dépot
def ajout_domicile(TasksDico, EmployeesDico):
    TasksEnhanced = TasksDico.copy()
    for row in EmployeesDico:
        # ajout d'une tâche au départ du domicile
        TasksEnhanced.append({'TaskId': 'Depart' + row['EmployeeName'], 'Latitude': row['Latitude'],    'Longitude': row['Longitude'],
                              'TaskDuration': 0, 'Skill': row['Skill'], 'Level': 0, 'OpeningTime': row['WorkingStartTime'], 'ClosingTime': row['WorkingEndTime']})
    for row in EmployeesDico:
        # ajout de l'arrivée au domicile
        TasksEnhanced.append({'TaskId': 'Arrivee'+row['EmployeeName'], 'Latitude': row['Latitude'],    'Longitude': row['Longitude'],
                              'TaskDuration': 0, 'Skill': row['Skill'], 'Level': 0, 'OpeningTime': row['WorkingStartTime'], 'ClosingTime': row['WorkingEndTime']})
    return(TasksEnhanced)

# Calculs à faire en fonction des tâches et des employes dico


def optimisation_1(C, nbre_employe, nbre_taches, D, Duree, Debut, Fin):

    m = Model("Modele exact simple")
    # -- ajout variables de décisions --
    M = 1440  # majorant des temps
    H = m.addMVar(shape=nbre_taches+2*nbre_employe, lb=0, ub=M)
    # Y = m.addMVar(shape=(nbre_employe, nbre_taches+2 *
    #                      nbre_employe, nbre_taches+2*nbre_employe), lb=0)
    X = m.addMVar(shape=(nbre_employe, nbre_taches+2*nbre_employe,
                         nbre_taches+2*nbre_employe),  vtype=GRB.BINARY)
    # modification des types des variables d'entrées pour s'assurer qu'elles conviennent
    C = np.array(C)
    D = np.array(D)

    #
    # taille du tableau modifié = nombre de tâches réelles + nombre de tâches fictives
    t = len(Debut)
    # -- Ajout des constraintes --

    # chaque trajet a bien été fait une seule fois
    for i in range(t):
        m.addConstr(sum(X[n, i, j] for n in range(nbre_employe)
                        for j in range(t)) == 1)  # fait sur les lignes. Devrait être fait sur les colonnes ?
    
    # Toute tâche à un départ et une arrivée faites par la même personne - INCOMPATIBLE BORDS
    for n in range(nbre_employe):
        for j in range(nbre_taches):
            m.addConstr(sum(X[n, j, k] for k in range(t)) == sum(
                X[n, i, j] for i in range(t)))
    
    # effets de bord
    for n in range(nbre_employe):
        m.addConstr(sum(X[n, nbre_taches+n, j]
                        for j in range(nbre_taches)) == 1)  # depart du depot
        m.addConstr(sum(X[n, i, nbre_taches+nbre_employe+n]
                        for i in range(nbre_taches)) == 1)  # arrivee au depot

    for i in range(t):  # Taches réelles + taches fictives
        for j in range(t):
            for n in range(nbre_employe):
                # l'employé doit être capable d'effectuer les 2 tâches
                m.addConstr(X[n, i, j] <= C[n, i])
                m.addConstr(X[n, i, j] <= C[n, j])

                # l'employé ne peut pas faire le trajet d'une tache vers elle-même : la diagonale doit être nulle
                m.addConstr(X[n, i, i] == 0)

                # - Effets temporels -
                # la tache j sera bien faite dans l'intervalle de temps ou elle est ouverte
                m.addConstr(H[j]+Duree[j] <= Fin[j])
                m.addConstr(H[j] >= Debut[j])
                # la personne n a le temps de faire la tache j à la suite de la tache i
                m.addConstr(X[n, i, j] * (H[i]+Duree[i]+D[i, j]/0.83333)
                            <= H[j])  # 
                # 0.833 = vitesse des ouvriers en km.min-1 (équivaut à 50km.h-1)
                # m.addConstr(Y[n, i, j]+X[n, i, j] *
                #             (Duree[i]+D[i, j]/0.83333) <= H[j])
                # m.addConstr(Y[n, i, j] <= H[i])
                # m.addConstr(Y[n, i, j] <= X[n, i, j]*M)
                # m.addConstr(Y[n, i, j] >= H[i]-M*(1-X[n, i, j]))

    # -- Ajout de la fonction objectif. Produit terme à terme
    m.setObjective(sum(X[n, i, j]*D[i, j] for n in range(nbre_employe)
                       for i in range(t) for j in range(t)), GRB.MINIMIZE)

    m.update()  # Mise à jour du modèle
    m.optimize()  # Résolution

    # -- Affichage des solutions --
    print("Les solutions optimales sont")
    print("X =", X.x)
    print("H =", H.x)
    print("avec pour valeur de l'objectif z =", m.objVal)
    return X.x, H.x, m.objVal
