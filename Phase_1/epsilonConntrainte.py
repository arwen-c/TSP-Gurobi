from opti_1 import optimisation_1


def epsilon_contrainte(fonctionObjectif, Capacite, nbre_employe, nbre_taches, tab_distance, Duree, Debut, Fin, ntR):
    # fonctionObjectif vaut 1 si on optimise la fonction objectif numéro 1, avec la deuxième fonction bornée, et vaut 2 si c'est l'inverse
    epsilon = 10
    borne = math.inf
    valeurObjectifs = []
    valeurBornes = []
    possible = True
    while possible:
        try:
            solution = optimisation_1(Capacite, nbre_employe,
                                      nbre_taches, tab_distance, Duree, Debut, Fin, ntR, borne, fonctionObjectif)
            borne = solution[3]-epsilon
            valeurObjectifs.append(solution[2])
            valeurBornes.append(solution[3])
            break
        except gurobipy.GurobiError:  # si on ne trouve plus de solution avec la borne imposée sur l'une des fonctions objectifs
            possible = False
        # solution[3] = f1(solution)
    return valeurObjectifs, valeurBornes
