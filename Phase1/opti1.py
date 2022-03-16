# Importations de module
from conda import CONDA_PACKAGE_ROOT
import numpy as np
from gurobipy import *


def ajoutDomicile(tasksDico, employeesDico):
    """Modification des données pour insérer des tâches factices de départ et de retour au dépot ou domicile."""
    tasksEnhanced = tasksDico.copy()
    for row in employeesDico:
        # ajout d'une tâche au départ du domicile
        tasksEnhanced.append({'TaskId': 'Depart' + row['EmployeeName'], 'Latitude': row['Latitude'],    'Longitude': row['Longitude'],
                              'TaskDuration': 0, 'Skill': row['Skill'], 'Level': 0, 'OpeningTime': row['WorkingStartTime'], 'ClosingTime': row['WorkingEndTime']})
    for row in employeesDico:
        # ajout de l'arrivée au domicile
        tasksEnhanced.append({'TaskId': 'Arrivee'+row['EmployeeName'], 'Latitude': row['Latitude'],    'Longitude': row['Longitude'],
                              'TaskDuration': 0, 'Skill': row['Skill'], 'Level': 0, 'OpeningTime': row['WorkingStartTime'], 'ClosingTime': row['WorkingEndTime']})
    return(tasksEnhanced)


def optimisation1(capcite, nbreEmploye, nbreTaches, distance, duree, debut, fin):
    """Variables dont on hérite des programmes précédents :
    capacite = matrice des capacité de l'ouvrier n à faire la tache i ;
    distance = matrice contenant la distance entre les tâches i et j en position (i,j) ;
    duree = liste des durées des tâches ;
    debut = liste des horaires de début des tâches ;
    fin = liste des horaires de fin des tâches."""

    # -- Création du modèle --
    m = Model("Modele exact simple")

    # -- Ajout variables de décisions --
    M = 1440  # majorant des temps
    H = m.addMVar(shape=nbreTaches+2*nbreEmploye, lb=0, ub=M)
    X = m.addMVar(shape=(nbreEmploye, nbreTaches+2*nbreEmploye,
                         nbreTaches+2*nbreEmploye),  vtype=GRB.BINARY)
    Y = m.addMVar(shape=(nbreEmploye, nbreTaches+2*nbreEmploye,
                         nbreTaches+2*nbreEmploye),  vtype=GRB.CONTINUOUS, lb=0)

    # -- Modification des types des variables d'entrées pour s'assurer qu'elles conviennent --
    capacite = np.array(capacite)
    distance = np.array(distance)

    # -- Taille du tableau modifié = nombre de tâches réelles + nombre de tâches fictives --
    t = len(debut)

    # -- Ajout des constraintes --

    # Chaque trajet a bien été fait une seule fois
    for i in range(t):
        m.addConstr(sum(X[n, i, j] for n in range(nbreEmploye)
                        for j in range(t)) == 1)

    # Toute tâche a un départ et une arrivée faite par la même personne, cette condition n'est pas appliquée au départ et à l'arrivée
    for n in range(nbreEmploye):
        for j in range(nbreTaches):
            m.addConstr(sum(X[n, j, k] for k in range(t)) == sum(
                X[n, i, j] for i in range(t)))

    # Effets de bord
    for n in range(nbreEmploye):
        m.addConstr(sum(X[n, nbreTaches+n, j]
                        for j in range(nbreTaches)) == 1)  # départ du dépôt
        m.addConstr(sum(X[n, i, nbreTaches+nbreEmploye+n]
                        for i in range(nbreTaches)) == 1)  # arrivée au dépôt

    # Contraintes incluants une somme
    for i in range(t):  # Tâches réelles + Tâches fictives
        for j in range(t):
            for n in range(nbreEmploye):
                # l'employé doit être capable d'effectuer les 2 tâches
                m.addConstr(X[n, i, j] <= capacite[n, i])
                m.addConstr(X[n, i, j] <= capacite[n, j])

                # l'employé ne peut pas faire le trajet d'une tache vers elle-même : la diagonale doit être nulle
                m.addConstr(X[n, i, i] == 0)

                # - Effets temporels -
                # la tache j sera bien faite dans l'intervalle de temps ou elle est ouverte
                m.addConstr(H[j]+duree[j] <= fin[j])
                m.addConstr(H[j] >= debut[j])
                # la personne n a le temps de faire la tache j à la suite de la tache i
                # m.addConstr(X[n, i, j] * (H[i]+Duree[i]+D[i, j]/0.83333)
                #             <= H[j])
                m.addConstr(H[i]+X[n, i, j]*(duree[i]+distance[i, j] /
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
    m.setObjective(sum(X[n, i, j]*distance[i, j]/0.833 for n in range(nbreEmploye)
                       for i in range(t) for j in range(t)), GRB.MINIMIZE)

    m.update()  # Mise à jour du modèle
    m.optimize()  # Résolution

    # -- Affichage des solutions --
    return X.x, H.x, m.objVal
