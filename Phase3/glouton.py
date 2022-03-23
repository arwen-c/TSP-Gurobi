import numpy as np
from sympy import E


def optiGlouton(matCapacite, matDistance, vecDuree, vecDebut, vecFin, dicoEmployes, dicoTachesEtendues):

    nombreEmployes = len(dicoEmployes)
    nombreTachesTotal = len(dicoTachesEtendues)
    X = np.zeros(nombreEmployes, nombreTachesTotal, nombreTachesTotal)
    L = np.zeros(nombreEmployes, nombreTachesTotal, nombreTachesTotal)
    H = np.zeros(nombreTachesTotal)
    for n in range(nombreEmployes):
        employe = dicoEmployes[n]
        t = employe['StartTime']
        finJourneeEmploye = employe['EndTime']
        localisationCourante = (employe['Longitude'], employe['Latitude'])
        pauseFaite = False
        # contrainte compétence, on obtient une liste de tâches qui ainsi limite les recherches inutiles
        tachesFaisables = fonctionCompetences(employe['Skill'], matCapacite)
        dicoIndis = fonctionRecuperationIndis(dicoTachesEtendues)
        while t < finJourneeEmploye:  # on construit la journée d'un employé au fur et à mesure
            # on regarde les tâches ouvertes au temps t ou qui vont s'ouvrir
            listeTachesPossibles = fonctionTachesPossibles(
                t, localisationCourante, matDistance, vecDuree, vecDebut, vecFin, employe, tachesFaisables)
            nombreTachesPossibles = len(listeTachesPossibles)
            if nombreTachesPossibles > 0:
                prochaineTacheTrouvee = False
                i = 0
                while not(prochaineTacheTrouvee) and i < nombreTachesPossibles:
                    prochaineTacheTrouvee, idTache = verificationContrainteIndisponibilites(
                        dicoIndis, listeTachesPossibles[i])
                if prochaineTacheTrouvee:
                    t += vecDuree[idTache]
                    X[n, idTachePrecedente, idTache] =
                elif not(pauseFaite) and t < 840:
                    pauseFaite = True
                    t += 45
                elif

    return X, H, L, valeurObjectif
