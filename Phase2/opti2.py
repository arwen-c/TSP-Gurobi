# Importations de module
import numpy as np
from gurobipy import *
from usefulFunctions2 import recuperationHeure


def ajoutTachesFictives(TasksDico, EmployeesDico, EmployeesUnavailDico):

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

        debut = recuperationHeure(row["Start"])
        fin = recuperationHeure(row["End"])

        TasksEnhanced.append({'TaskId': 'Unavail' + row['EmployeeName'], 'Latitude': row['Latitude'],    'Longitude': row['Longitude'],
                              'TaskDuration': fin-debut, 'Skill': None, 'Level': 0, 'OpeningTime': row['Start'], 'ClosingTime': row['End']})

    return(TasksEnhanced)


def optimisation2(C, nbre_employe, nbre_taches, nbreIndispoEmploye, D, Duree, Debut, Fin, EmployeesDico, TasksEnhanced, borne, fonctionObjectif):
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

    # -- Taille du tableau modifié = nombre de tâches réelles + nombre de tâches fictives --
    t = len(Debut)

    nbreIndisMax = max(len(Fin[j]) for j in range(t))

    H = m.addMVar(shape=nbre_taches+2*nbre_employe +
                  nbreIndispoEmploye, lb=0, ub=M)
    X = m.addMVar(shape=(nbre_employe, nbre_taches+2*nbre_employe+nbreIndispoEmploye,
                         nbre_taches+2*nbre_employe+nbreIndispoEmploye),  vtype=GRB.BINARY)
    L = m.addMVar(shape=(nbre_employe, nbre_taches,
                         nbre_taches), vtype=GRB.BINARY)
    delta = m.addMVar(shape=(nbre_taches+2*nbre_employe +
                             nbreIndispoEmploye, nbreIndisMax), vtype=GRB.BINARY)

    # -- Modification des types des variables d'entrées pour s'assurer qu'elles conviennent --
    C = np.array(C)
    D = np.array(D)

    # -- Ajout des contraintes --

    # Chaque trajet a bien été fait une seule fois
    # Ancienne contrainte
    # for i in range(t):
    #     m.addConstr(sum(X[n, i, j] for n in range(nbre_employe)
    #                     for j in range(t)) == 1)

    # nouvelle contrainte
    for i in range(t):
        m.addConstr(sum(X[n, i, j] for n in range(nbre_employe)
                        for j in range(t)) <= 1)

    # Toute tâche a un départ et une arrivée faite par la même personne, cette condition n'est pas appliquée au départ et à l'arrivée
    for n in range(nbre_employe):
        for j in range(nbre_taches):
            m.addConstr(sum(X[n, j, k] for k in range(t)) == sum(
                X[n, i, j] for i in range(t)))

        # Les employés font bien leurs pauses (indisponibilités):
    for n in range(nbre_employe):
        NomEmploye = EmployeesDico[n]['EmployeeName']
        #print("nbreIndispoEmploye :{}".format(nbreIndispoEmploye))
        for i_unavail in range(nbreIndispoEmploye):
            # Il faut que ce soit le bon employé qui fasse la pause
            if TasksEnhanced[nbre_taches+2*nbre_employe+i_unavail]['TaskId'] == "Unavail" + NomEmploye:
                m.addConstr(sum(X[n, i, nbre_taches+2*nbre_employe+i_unavail]
                                for i in range(nbre_taches)) == 1)  # arrivé à la pause
                m.addConstr(sum(X[n, nbre_taches+2*nbre_employe+i_unavail, i]
                                for i in range(nbre_taches)) == 1)  # départ de la pause
                #print("TasksEnhanced[nbre_taches+2*nbre_employe+i_unavail]['TaskId'] : {}".format(TasksEnhanced[nbre_taches+2 *nbre_employe+i_unavail]['TaskId']))
            else:  # Un autre ne peux pas piquer la pause d'un autre
                m.addConstr(sum(X[n, i, nbre_taches+2*nbre_employe+i_unavail]
                                for i in range(nbre_taches)) == 0)  # arrivé à la pause

    # Effets de bord
    for n in range(nbre_employe):
        m.addConstr(sum(X[n, nbre_taches+n, j]
                        for j in range(nbre_taches)) == 1)  # départ du dépôt
        m.addConstr(sum(X[n, i, nbre_taches+nbre_employe+n]
                        for i in range(nbre_taches)) == 1)  # arrivée au dépôt

    # Ajout des contraintes sur L
    # Une pause dej n'est possible qu'entre deux taches réalisées
    for n in range(nbre_employe):
        for i in range(nbre_taches):
            for j in range(nbre_taches):
                m.addConstr(L[n, i, j] <= X[n, i, j])
    # Une personne fait une et une seule pause dej
        m.addConstr(sum(L[n, i, j] for i in range(nbre_taches)
                        for j in range(nbre_taches)) == 1)

    for i in range(t):  # Tâches réelles + Tâches fictives
        for j in range(t):
            for n in range(nbre_employe):
                # l'employé doit être capable d'effectuer les 2 tâches
                m.addConstr(X[n, i, j] <= C[n, i])
                m.addConstr(X[n, i, j] <= C[n, j])

                # l'employé ne peut pas faire le trajet d'une tache vers elle-même : la diagonale doit être nulle
                #m.addConstr(X[n, i, i] == 0)

                # - Effets temporels -
                # la tache j sera bien faite dans un intervalle de temps où elle est ouverte
                nbreCreneauxJ = len(Fin[j])

                for k in range(nbreCreneauxJ):
                    # -?M(1-delta) <= x-x0 <= M.delta       x0<x SSI delta>1
                    m.addConstr(-M*(1-delta[j, k]) <= H[j]-Debut[j][k])
                    m.addConstr(H[j]-Debut[j][k] <= M*delta[j, k])
                    # -M(1-delta) <= x1-x <= M.delta      x<x1 SSI delta>1
                    m.addConstr(-M*(1-delta[j, k])
                                <= -H[j]+Fin[j][k]-Duree[j])
                    m.addConstr(-H[j]+Fin[j][k]-Duree[j] <= M*delta[j, k])

                # On ne va pas faire plusieurs fois la même tâche
                m.addConstr(sum(delta[j, k]
                                for k in range(nbreCreneauxJ)) == 1)

                # Contraintes pour avoir les pauses déjeuner entre 12h et 14 h

                # la personne n a le temps de faire la tache j à la suite de la tache i et peut etre de faire sa pause déjeuner
                if i < nbre_taches and j < nbre_taches:  # on est entre deux tâches réelles
                    m.addConstr(H[i] + X[n, i, j] * (Duree[i]+D[i, j]/0.833) + L[n, i, j]*60
                                <= H[j] + 24*60*(1-X[n, i, j]))
                    m.addConstr(H[i]+Duree[i] <= 13*60 + (1-L[n, i, j])*60*11)
                    m.addConstr(13*60-(1-L[n, i, j])*60*13 <= H[j])
                    None

                else:
                    m.addConstr(
                        H[i] + X[n, i, j] * (Duree[i]+D[i, j]/0.833) <= H[j] + 24*60*(1-X[n, i, j]))
                # 0.833 = vitesse des ouvriers en km.min-1 (équivaut à 50km.h-1)

    # -- Ajout de la fonction objectif.
    ntR = len(TasksEnhanced)

    # Optimisation sur f1

    if fonctionObjectif == 1:
        m.addConstr(-sum(X[n, i, j]*Duree[i] for n in range(nbre_employe)
                         for i in range(ntR) for j in range(t)) <= borne)
        m.setObjective(sum(X[n, i, j]*D[i, j] for n in range(nbre_employe)
                           for i in range(t) for j in range(t)), GRB.MINIMIZE)
    # Optimisation sur f2
    elif fonctionObjectif == 2:
        m.addConstr(sum(X[n, i, j]*D[i, j] for n in range(nbre_employe)
                        for i in range(t) for j in range(t)) <= borne)
        m.setObjective(-sum(X[n, i, j]*Duree[i] for n in range(nbre_employe)
                            for i in range(ntR) for j in range(t)), GRB.MINIMIZE)
  #  m.params.outputflag = 0
    m.update()  # Mise à jour du modèle
    m.optimize()  # Résolution

    # Calcul de la valeur de l'autre fonction objectif

    valeur = 0
    if fonctionObjectif == 1:
        nbre, x, y = X.x.shape
        for n in range(nbre):
            for i in range(x):
                for j in range(y):
                    valeur += X.x[n, i, j]*Duree[i]
        return X.x, H.x, L.x, m.objVal, valeur

    elif fonctionObjectif == 2:
        nbre, x, y = X.x.shape
        for n in range(nbre):
            for i in range(x):
                for j in range(y):
                    valeur += X.x[n, i, j]*D[i, j]
        return X.x, H.x, L.x, m.objVal, valeur
