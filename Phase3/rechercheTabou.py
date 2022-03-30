from glouton import *

# question : comment caractériser une solution ? Par la matrice des X ? Ca rend la comparaison entre plusieurs solutions assez laborieuse pour de grandes instances
# quel critère d'arrêt ? pour une première version, utilisation d'un nombre d'itération maximum. Par la suite, on peut améliorer le programme en utilisant un nombre max d'itération depuis la dernière mise à jour d'un minimum (dernier ajout à la liste tabou)
# d'autres améliorations, notamment sur la tailleMemoire sont proposées dans le poly de métaheuristique


def rechercheTabou(capacite, matDistance, duree, debut, fin, nbreTaches, employeesDico, indispoDico, tachesDico, tailleMemoire):
    solution = optiGlouton(capacite, matDistance, duree, debut,
                           fin, nbreTaches, employeesDico, indispoDico, tachesDico)
    memoire = []
    posMemoire = 0
    continu = True  # critère d'arrêt : nombre d'itération max autorisé de 1000
    iteration = 0
    while continu:
        solutionTemp = meilleurVoisin(solution, memoire)
        if cout(solutionTemp) < cout(solution):
            if len(memoire) < tailleMemoire:
                memoire.append(solution)
            else:
                memoire[posMemoire] = solution
                posMemoire = (posMemoire+1) % tailleMemoire
        solution = solutionTemp
        iteration += 1
        if iteration > 1000:
            continu = False
    return optimum(memoire)


def meilleurVoisin(solution, memoire):
    # retourne le voisin ayant le meilleur cout parmi l'ensemble des voisins n'étant pas dans mémoire
    return solution


def cout(solution):
    # calcule le cout (et donc l'optimialité) associée à une solution. Un cout arbitrairement élevé est appliqué pour une solution non faisable.
    return "gratuit !- pour l'instant"


def optimum(tableau):
    # retourne la solution ayant le cout le plus intéressant des solutions stockées en mémoire
    min, indMin = -1, -1
    for i in range(len(tableau)):
        if cout(tableau[i]) < min or min == -1:
            min = cout(tableau[i])
            indMin = i
    return tableau[indMin]
