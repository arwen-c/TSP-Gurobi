from matplotlib import fontconfig_pattern
from opti_1 import optimisation_1
from math import inf
import matplotlib.pyplot as plt


def epsilonContrainte(fonctionObjectif, Capacite, nbre_employe, nbre_taches, tab_distance, Duree, Debut, Fin, ntR):
    # fonctionObjectif vaut 1 si on optimise la fonction objectif numéro 1, avec la deuxième fonction bornée, et vaut 2 si c'est l'inverse
    epsilon = 10
    borne = 1000000
    valeurObjectifs = []
    valeurBornes = []
    possible = True
    print("La borne vaut : {}".format(borne))
    while possible:
        try:
            solution = optimisation_1(Capacite, nbre_employe,
                                      nbre_taches, tab_distance, Duree, Debut, Fin, ntR, borne, fonctionObjectif)
            borne = solution[3]-epsilon
            print("La borne vaut : {}".format(borne))
            valeurObjectifs.append(solution[2])
            valeurBornes.append(solution[3])
            break
        except gurobipy.GurobiError:  # si on ne trouve plus de solution avec la borne imposée sur l'une des fonctions objectifs
            possible = False
        # solution[3] = f1(solution)
    return valeurObjectifs, valeurBornes


def plotSolutions1(fonctionObjectif, valeurObjectifs, valeurBornes):
    plt.plot(valeurObjectifs, valeurBornes, "-o")
    plt.title("Optimisation sur : "+str(fonctionObjectif))
    plt.show()


def plotSolutions2(Capacite, nbre_employe, nbre_taches, tab_distance, Duree, Debut, Fin, ntR):
    fonctionObjectif = 1
    valeurObjectifs, valeurBornes = epsilonContrainte(
        fonctionObjectif, Capacite, nbre_employe, nbre_taches, tab_distance, Duree, Debut, Fin, ntR)
    plt.plot(valeurObjectifs, valeurBornes, "-o")
    fonctionObjectif = 2
    valeurObjectifs, valeurBornes = epsilonContrainte(
        fonctionObjectif, Capacite, nbre_employe, nbre_taches, tab_distance, Duree, Debut, Fin, ntR)
    plt.plot(valeurObjectifs, valeurBornes, "-o")
    plt.title("Optimisation bi objectif")
    plt.show()
