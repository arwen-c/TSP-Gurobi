import matplotlib.pyplot as plt
from usefulFunctions1 import extractionData


def affichageGraphiqueTest(latitudes, longitudes):

    employee1 = [1, 3, 8, 9]
    employee2 = [2, 4, 5, 6, 7]

    longitude1 = [longitudes[i] for i in employee1]
    lattitude1 = [latitudes[i] for i in employee1]
    longitude2 = [longitudes[i] for i in employee2]
    lattitude2 = [latitudes[i] for i in employee2]
    plt.plot(longitude1, lattitude1, "-o", color="g")
    plt.plot(longitude2, lattitude2, "-o", color="b")
    plt.plot()
    plt.show()

    return None

# Améliorations :
# utiliser une couleur par employé pour les parcours
# afficher le numéro de la tâche
# mettre une flèche dans le sens de parcours
# dessiner une petite maison dans la prairie
# mettre un fond de carte maps


latitudes = [44.556549383420084,
             44.967500952177986,
             45.14421541464031,
             45.264808304867096,
             45.044422793402624,
             45.19957452440505,
             45.397697776585,
             45.023479086796385,
             45.29291368453335,
             45.08146166752168,
             ]

longitudes = [-0.31939224223757195,
              -0.6086852638150881,
              -0.7342570469020379,
              -0.7717887212411139,
              -0.6687606009488057,
              -0.7462077931750715,
              -0.9668192708194538,
              -0.8072126299796225,
              -0.9365361007032235,
              -0.8062453230620741]

# affichageGraphiqueTest(latitudes, longitudes)


def lecture(filename):

    # lecture du fichier solution
    fichierSolution = open(filename, "r")
    mot = ''
    taches = []
    employes = []
    horairesDebut = []
    for ligne in fichierSolution.readlines()[1:]:
        compte = 0
        # print("ligne : {}".format(ligne))
        for element in ligne:
            if element == ";":
                # print(mot)
                compte += 1
                if compte == 1:  # si le mot est le numéro de la tâche
                    # print("\n mot : {} - tâches : {}".format(mot, taches))
                    # print("mot : {} - len : {}".format(mot, len(mot)))
                    if len(mot) == 3:
                        taches += [mot[1:3]]
                    elif len(mot) == 4:
                        taches += [mot[1:4]]
                    else:
                        taches += [mot]
                elif compte == 3:  # si le mot est le nom de l'employee
                    employes = employes + [mot]
                    # print("mot : {}".format(mot))
                    # print("employé : {}".format(employes))
                elif compte == 4:  # si le mot est l'heure de début
                    horairesDebut = horairesDebut + [mot]
                mot = ''
            else:
                mot += element
    return employes, taches, horairesDebut


def extraireCoordonnees(path):
    employeesDico, tasksDico = extractionData(path)
    return vecteurLongitudes(tasksDico), vecteurLatitudes(tasksDico), vecteurLongitudes(employeesDico), vecteurLatitudes(employeesDico)

# Vecteur des longitudes


def vecteurLongitudes(tasksDico):
    """Renvoie le vecteur des longitudes de chaque tâche."""
    vecteurLong = []
    for row in tasksDico:
        vecteurLong.append(row['Longitude'])
    return vecteurLong

# Vecteur des latitudes


def vecteurLatitudes(tasksDico):
    """Renvoie le vecteur des latitudes de chaque tâche."""
    vecteurLat = []
    for row in tasksDico:
        vecteurLat.append(row['Latitude'])
    return vecteurLat


# tri de listeAOrdonner par ordre décroissant sur la listeUtilePourOrdre
def ordreDecListe(listeAOrdonner, listeUtilePourOrdre):
    if len(listeUtilePourOrdre) != len(listeAOrdonner):
        return "Erreur : les listes à trier ne sont pas de la même dimension"
    listeUtilePourOrdre_2 = listeUtilePourOrdre.copy()
    order = [i for i in range(len(listeUtilePourOrdre_2))]
    i = 0
    while i < len(listeUtilePourOrdre_2) - 1:
        if listeUtilePourOrdre_2[i] > listeUtilePourOrdre_2[i+1]:
            listeUtilePourOrdre_2[i], listeUtilePourOrdre_2[i +
                                                            1] = listeUtilePourOrdre_2[i+1], listeUtilePourOrdre_2[i]
            order[i], order[i+1] = order[i+1], order[i]
            i = -1
        i = i + 1

    listeAOrdonner2 = [listeAOrdonner[indice] for indice in order]

    return listeAOrdonner2


def affichageGraphique(longitudes, latitudes, longEmploye, latEmploye, employes, taches, horairesDebut, nomVille):
    employesUnique = []
    for employe in employes:
        if employe not in employesUnique:
            employesUnique += [employe]

    mesCouleurs = ["r", "g", "b", "c", "m", "y",
                   "k", "r", "g", "b", "c", "m", "y", "k"]
    for i in range(len(employesUnique)):

        longitudesEmploye = [longitudes[j] for j in range(
            len(employes)) if employes[j] == employesUnique[i]]
        latitudesEmploye = [latitudes[j] for j in range(
            len(employes)) if employes[j] == employesUnique[i]]

        horaireDebutEmploye = [horairesDebut[j] for j in range(
            len(employes)) if employes[j] == employesUnique[i]]

        # On trie les longitudes/latitudes des tâches des employés par ordre croissant de début de leurs tâches

        latitudesEmploye = ordreDecListe(
            latitudesEmploye, horaireDebutEmploye)
        longitudesEmploye = ordreDecListe(
            longitudesEmploye, horaireDebutEmploye)

        # Attention, ça marche que si les employés ont le même domicile
        longitudesEmploye.insert(0, longEmploye[0])
        latitudesEmploye.insert(0, latEmploye[0])
        longitudesEmploye += [longEmploye[0]]
        latitudesEmploye += [latEmploye[0]]

        plt.plot(longitudesEmploye, latitudesEmploye,
                 "-o", color=mesCouleurs[i], label=str(employesUnique[i]))
        for j in range(len(employes)):
            if employes[j] == employesUnique[i]:
                plt.annotate(str(taches[j]),
                             (longitudes[j], latitudes[j]))

    plt.title(str(nomVille))
    plt.legend()
    plt.show()
    return None


# longitudes, latitudes = extraireCoordonnees(path='InstanceBordeauxV1.xlsx')


# affichageGraphique(longitudes, latitudes, lecture("SolutionBordeauxV1ByV1.txt")[
#                     0], lecture("SolutionBordeauxV1ByV1.txt")[1])


def afficher(nomVille):
    path1 = "Phase1/InstancesV1/Instance"+str(nomVille)+"V1.xlsx"
    path2 = "Phase1/Solutions/Solution"+str(nomVille)+"V1ByV1.txt"

    longitudes, latitudes, longEmploye, latEmploye = extraireCoordonnees(
        path=path1)
    employes, taches, horairesDebut = lecture(path2)

    affichageGraphique(longitudes, latitudes, longEmploye,
                       latEmploye, employes, taches, horairesDebut, nomVille)
    return None


afficher("Poland")
