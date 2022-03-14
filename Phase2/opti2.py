# Import de modules
import numpy as np
from gurobipy import *


def ajoutTachesFictives(TasksDico, EmployeesDico, EmployeesUnavailDico, TasksUnavailDico):

    # (rechercher ajout_domicile dans tous les docs pour modifier par ajout_taches_fictives)
    ### AJOUTS DOMICILES ###
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

    ### AJOUTS INDISPONIBILITES EMPLOYES ###
    for row in EmployeesUnavailDico:
        TasksEnhanced.append({'TaskId': 'Unavail' + row['EmployeeName'], 'Latitude': row['Latitude'],    'Longitude': row['Longitude'],
                              'TaskDuration': row['End']-row['Start'], 'Skill': None, 'Level': 0, 'OpeningTime': row['Start'], 'ClosingTime': row['End']})

    return(TasksEnhanced)


def optimisation2(C, nbre_employe, nbre_taches, nbreIndispoEmploye, D, Duree, Debut, Fin, temps_trajet, EmployeesDico, TasksEnhanced):
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
    X = m.addMVar(shape=(nbre_employe, nbre_taches+2*nbre_employe+nbreIndispoEmploye,
                         nbre_taches+2*nbre_employe+nbreIndispoEmploye),  vtype=GRB.BINARY)

    # -- Modification des types des variables d'entrées pour s'assurer qu'elles conviennent --
    C = np.array(C)
    D = np.array(D)

    # -- Taille du tableau modifié = nombre de tâches réelles + nombre de tâches fictives --
    t = len(Debut)

    # -- Ajout des constraintes --

#     # Chaque trajet a bien été fait une seule fois
#     for i in range(t):
#         m.addConstr(sum(X[n, i, j] for n in range(nbre_employe)
#                         for j in range(t)) == 1)

#     # Toute tâche a un départ et une arrivée faite par la même personne, cette condition n'est pas appliquée au départ et à l'arrivée
#     for n in range(nbre_employe):
#         for j in range(nbre_taches):
#             m.addConstr(sum(X[n, j, k] for k in range(t)) == sum(
#                 X[n, i, j] for i in range(t)))

    # Les employés font bien leur pauses :
    for n in range(nbre_employe):
        NomEmploye = EmployeesDico[n]['EmployeeName']
        for i_unavail in range(nbreIndispoEmploye):
            # Il faut que ce soit le bon employé qui fasse la pause
            if TasksEnhanced[nbre_taches+2*nbre_employe+i_unavail]['TaskId'] == "Unavail" + NomEmploye:
                m.addConstr(sum(X[n, i, nbre_taches+2*nbre_employe+i_unavail]
                                for i in range(nbre_taches)) == 1)  # arrivé à la pause
            else:  # Un autre ne peux pas piquer la pause d'un autre
                m.addConstr(sum(X[n, i, nbre_taches+2*nbre_employe+i_unavail]
                                for i in range(nbre_taches)) == 0)  # arrivé à la pause


#     # Effets de bord
#     for n in range(nbre_employe):
#         m.addConstr(sum(X[n, nbre_taches+n, j]
#                         for j in range(nbre_taches)) == 1)  # départ du dépôt
#         m.addConstr(sum(X[n, i, nbre_taches+nbre_employe+n]
#                         for i in range(nbre_taches)) == 1)  # arrivée au dépôt

#     # Contraintes incluants une somme
#     for i in range(t):  # Tâches réelles + Tâches fictives
#         for j in range(t):
#             for n in range(nbre_employe):
#                 # l'employé doit être capable d'effectuer les 2 tâches
#                 m.addConstr(X[n, i, j] <= C[n, i])
#                 m.addConstr(X[n, i, j] <= C[n, j])

#                 # l'employé ne peut pas faire le trajet d'une tache vers elle-même : la diagonale doit être nulle
#                 m.addConstr(X[n, i, i] == 0)

#                 # - Effets temporels -
#                 # la tache j sera bien faite dans l'intervalle de temps ou elle est ouverte
#                 m.addConstr(H[j]+Duree[j] <= Fin[j])
#                 m.addConstr(H[j] >= Debut[j])
#                 # la personne n a le temps de faire la tache j à la suite de la tache i
#                 m.addConstr(X[n, i, j] * (H[i]+Duree[i]+temps_trajet[i, j])
#                             <= H[j])
#                 # 0.833 = vitesse des ouvriers en km.min-1 (équivaut à 50km.h-1)

#     # -- Ajout de la fonction objectif.
#     # Produit terme à terme
#     m.setObjective(sum(X[n, i, j]*temps_trajet[i, j] for n in range(nbre_employe)
#                        for i in range(t) for j in range(t)), GRB.MINIMIZE)

#     m.update()  # Mise à jour du modèle
#     m.optimize()  # Résolution

#     # -- Affichage des solutions --
#     return X.x, H.x, m.objVal
