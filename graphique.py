import matplotlib.pyplot as plt


def affichage_graphique_test(lattitudes, longitudes):

    employee_1 = [1, 3, 8, 9]
    employee_2 = [2, 4, 5, 6, 7]

    longitudes_1 = [longitudes[i] for i in employee_1]
    lattitudes_1 = [lattitudes[i] for i in employee_1]
    longitudes_2 = [longitudes[i] for i in employee_2]
    lattitudes_2 = [lattitudes[i] for i in employee_2]
    plt.plot(longitudes_1, lattitudes_1, "-o", color="g")
    plt.plot(longitudes_2, lattitudes_2, "-o", color="b")
    plt.plot()
    plt.show()

    return None

# Améliorations :
# utiliser une couleur par employé pour les parcours
# afficher le numéro de la tâche
# mettre une flèche dans le sens de parcours
# dessiner une petite maison dans la prairie
# mettre un fond de carte maps


lattitudes = [44.556549383420084,
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

# affichage_graphique_test(lattitudes, longitudes)


def lecture(filename):

    # lecture du fichier solution
    solution_file = open(filename, "r")
    word = ''
    taches = []
    employes = []
    for line in solution_file.readlines()[1:]:
        count = 0
        # print("ligne : {}".format(line))
        for element in line:
            if element == ";":
                # print(word)
                count += 1
                if count == 1:
                    # print("\n word : {} - tâches : {}".format(word, taches))
                    # print("word : {} - len : {}".format(word, len(word)))
                    if len(word) == 3:
                        taches += [word[1:3]]
                    elif len(word) == 4:
                        taches += [word[1:4]]
                    else:
                        taches += [word]
                elif count == 3:
                    employes = employes + [word]
                    # print("word : {}".format(word))
                    # print("employé : {}".format(employes))
                word = ''
            else:
                word += element
    return employes, taches


def affichage_graphique(longitudes, lattitudes, employes, taches):
    employes_unique = []
    for employe in employes:
        if employe not in employes_unique:
            employes_unique += [employe]

    my_colors = ["r", "g", "b"]
    for i in range(len(employes_unique)):
        # longitudes_employe = []
        # for j in range(len(employes)):
        #     if employes[j] == employes_unique[i]:
        #         longitudes_employe.append(longitudes[j])
        longitudes_employe = [longitudes[j] for j in range(
            len(employes)) if employes[j] == employes_unique[i]]
        lattitudes_employe = [lattitudes[j] for j in range(
            len(employes)) if employes[j] == employes_unique[i]]
        plt.plot(longitudes_employe, lattitudes_employe,
                 "-o", color=my_colors[i], label=str(employes_unique[i]))

    plt.legend()
    plt.show()
    return None


affichage_graphique(longitudes, lattitudes, lecture("SolutionBordeauxV1ByV1.txt")[
                    0], lecture("SolutionBordeauxV1ByV1.txt")[1])
