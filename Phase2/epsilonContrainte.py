from matplotlib import fontconfig_pattern
from opti2 import optimisation2
from math import inf
import matplotlib.pyplot as plt
from gurobipy import *


def epsilonContrainte(fonctionObjectif, Capacite, nbre_employe, nbre_taches, nbreIndispoEmploye, tab_distance, Duree, Debut, Fin, EmployeesDico, TasksEnhanced):
    # fonctionObjectif vaut 1 si on optimise la fonction objectif numéro 1, avec la deuxième fonction bornée, et vaut 2 si c'est l'inverse
    epsilon = 1
    borne = 1000000
    valeurObjectifs = []
    valeurBornes = []
    possible = True
    print("La borne vaut : {}".format(borne))
    while possible:
        try:
            solution = optimisation2(Capacite, nbre_employe,
                                     nbre_taches, nbreIndispoEmploye, tab_distance, Duree, Debut, Fin, EmployeesDico, TasksEnhanced, borne, fonctionObjectif)
            borne = solution[4]-epsilon
            print("La borne vaut : {}".format(borne))
            valeurObjectifs.append(solution[3])
            valeurBornes.append(solution[4])
            break
        except gurobipy.GurobiError:  # si on ne trouve plus de solution avec la borne imposée sur l'une des fonctions objectifs
            possible = False
        # solution[3] = f1(solution)
    return valeurObjectifs, valeurBornes


def plotSolutions1(fonctionObjectif, valeurObjectifs, valeurBornes):
    print("valeurObjectifs : {} et valeurBornes {}".format(
        valeurObjectifs, valeurBornes))
    plt.plot(valeurObjectifs, valeurBornes, "-o")
    plt.title("Optimisation sur : f"+str(fonctionObjectif))
    plt.show()


def plotSolutions2(Capacite, nbre_employe, nbre_taches, nbreIndispoEmploye, tab_distance, Duree, Debut, Fin, EmployeesDico, TasksEnhanced):
    fonctionObjectif = 1
    valeurObjectifs, valeurBornes = epsilonContrainte(
        fonctionObjectif, Capacite, nbre_employe, nbre_taches, nbreIndispoEmploye, tab_distance, Duree, Debut, Fin, EmployeesDico, TasksEnhanced)
    print("Pour la fonction objectif {}, valeurObjectifs : {} et valeurBornes : {}".format(
        fonctionObjectif, valeurObjectifs, valeurBornes))
    plt.plot(valeurObjectifs, valeurBornes, "-o")
    fonctionObjectif = 2
    valeurObjectifs, valeurBornes = epsilonContrainte(
        fonctionObjectif, Capacite, nbre_employe, nbre_taches, nbreIndispoEmploye, tab_distance, Duree, Debut, Fin, EmployeesDico, TasksEnhanced)
    print("Pour la fonction objectif {}, valeurObjectifs : {} et valeurBornes : {}".format(
        fonctionObjectif, valeurObjectifs, valeurBornes))
    plt.plot(valeurObjectifs, valeurBornes, "-o")
    plt.title("Optimisation bi objectif")
    plt.show()
