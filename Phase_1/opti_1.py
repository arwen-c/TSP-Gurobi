# Importations de module
import numpy as np
from gurobipy import *


def ajout_domicile(TasksDico, EmployeesDico):
    """Modification des données pour insérer des tâches factices de départ et de retour au dépot ou domicile."""
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


def optimisation_1(C, nbre_employe, nbre_taches, D, Duree, Debut, Fin, ntR, borne):
    """Variables dont on hérite des programmes précédents :
    C = matrice des capacité de l'ouvrier n à faire la tache i ;
    D = matrice contenant la distance entre les tâches i et j en position (i,j) ;
    Duree = liste des durées des tâches ;
    Debut = liste des horaires de début des tâches ;
    Fin = liste des horaires de fin des tâches."""

    # -- Création du modèle --
    m = Model("Modele exact simple")

    # -- Ajout variables de décisions --
    M = 1440  # majorant des temps
    H = m.addMVar(shape=nbre_taches+2*nbre_employe, lb=0, ub=M)
    X = m.addMVar(shape=(nbre_employe, nbre_taches+2*nbre_employe,
                         nbre_taches+2*nbre_employe),  vtype=GRB.BINARY)
    Y = m.addMVar(shape=(nbre_employe, nbre_taches+2*nbre_employe,
                         nbre_taches+2*nbre_employe),  vtype=GRB.CONTINUOUS, lb=0)

    # -- Modification des types des variables d'entrées pour s'assurer qu'elles conviennent --
    C = np.array(C)
    D = np.array(D)

    # -- Taille du tableau modifié = nombre de tâches réelles + nombre de tâches fictives --
    t = len(Debut)

    # -- Ajout des constraintes --

    # Chaque trajet a bien été fait une seule fois
    # Ancienne contrainte
    # for i in range(t):
    #     m.addConstr(sum(X[n, i, j] for n in range(nbre_employe)
    #                     for j in range(t)) == 1)
    # nouvelle contrainte
    for i in range(t):
        m.addConstr(sum(X[n, i, j] for n in range(nbre_employe)
                        for j in range(t)) == 1)

    # Toute tâche a un départ et une arrivée faite par la même personne, cette condition n'est pas appliquée au départ et à l'arrivée
    for n in range(nbre_employe):
        for j in range(nbre_taches):
            m.addConstr(sum(X[n, j, k] for k in range(t)) == sum(
                X[n, i, j] for i in range(t)))

    # Effets de bord
    for n in range(nbre_employe):
        m.addConstr(sum(X[n, nbre_taches+n, j]
                        for j in range(nbre_taches)) == 1)  # départ du dépôt
        m.addConstr(sum(X[n, i, nbre_taches+nbre_employe+n]
                        for i in range(nbre_taches)) == 1)  # arrivée au dépôt

    # Contraintes incluants une somme
    for i in range(t):  # Tâches réelles + Tâches fictives
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
                # m.addConstr(X[n, i, j] * (H[i]+Duree[i]+D[i, j]/0.83333)
                #             <= H[j])
                m.addConstr(H[i]+X[n, i, j]*(Duree[i]+D[i, j] /
                                             0.83333) <= H[j] + (1-X[n, i, j])*24*60)
                # m.addConstr(X[n, i, j] * H[i] == Y[n, i, j])
                # m.addConstr(H[i] >= Y[n, i, j])
                # m.addConstr(Y[n, i, j] <= X[n, i, j] * M)
                # m.addConstr(Y[n, i, j] >= H[i]-M*(1-X[n, i, j]))
                # m.addConstr(
                #     Y[n, i, j] + X[n, i, j] * (Duree[i]+D[i, j]/0.83333) <= H[j])
                # 0.833 = vitesse des ouvriers en km.min-1 (équivaut à 50km.h-1)

    # -- Ajout de la fonction objectif.
    # Produit terme à terme
    # f1
    # m.setObjective(sum(X[n, i, j]*D[i, j] for n in range(nbre_employe)
    #                    for i in range(t) for j in range(t)), GRB.MINIMIZE)
    # f2
    # Il faudra mettre le ntR dans le fichier "code_exe_2"
    # ntR = len(TasksDico)
    # epsilon = 400
    m.addConstr(sum(X[n, i, j]*D[i, j] for n in range(nbre_employe)
                    for i in range(t) for j in range(t)) <= borne)
    m.setObjective(sum(X[n, i, j]*Duree[i] for n in range(nbre_employe)
                       for i in range(ntR) for j in range(t)), GRB.MAXIMIZE)

    m.update()  # Mise à jour du modèle
    m.optimize()  # Résolution

    # -- Affichage des solutions --

    # return X.x, H.x, m.objVal, borne
    valeur = 0
    nbre, x, y = X.x.shape
    for n in range(nbre):
        for i in range(x):
            for j in range(y):
                valeur += X.x[n, i, j]*D[i, j]

    return X.x, H.x, m.objVal, valeur
