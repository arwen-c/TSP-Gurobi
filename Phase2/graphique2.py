import matplotlib.pyplot as plt
from firstdoc import extraction_data
import folium

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
    start_times = []
    for line in solution_file.readlines()[1:]:
        count = 0
        # print("ligne : {}".format(line))
        for element in line:
            if element == ";":
                # print(word)
                count += 1
                if count == 1:  # si le mot est le numéro de la tâche
                    # print("\n word : {} - tâches : {}".format(word, taches))
                    # print("word : {} - len : {}".format(word, len(word)))
                    if len(word) == 3:
                        taches += [word[1:3]]
                    elif len(word) == 4:
                        taches += [word[1:4]]
                    else:
                        taches += [word]
                elif count == 3:  # si le mot est le nom de l'employee
                    employes = employes + [word]
                    # print("word : {}".format(word))
                    # print("employé : {}".format(employes))
                elif count == 4:  # si le mot est l'heure de début
                    start_times = start_times + [word]
                word = ''
            else:
                word += element
    return employes, taches, start_times


def extraire_coordonnees(nom_ville):
    path="Phase_1/InstancesV1/Instance"+str(nom_ville)+"V1.xlsx"
    EmployeesDico, TasksDico = extraction_data(path)
    return vecteur_longitudes(TasksDico), vecteur_latitudes(TasksDico), vecteur_longitudes(EmployeesDico), vecteur_latitudes(EmployeesDico)

# Vecteur des longitudes


def vecteur_longitudes(TasksDico):
    """Renvoie le vecteur des longitudes de chaque tâche."""
    Vecteur_long = []
    for row in TasksDico:
        Vecteur_long.append(row['Longitude'])
    return Vecteur_long

# Vecteur des latitudes


def vecteur_latitudes(TasksDico):
    """Renvoie le vecteur des latitudes de chaque tâche."""
    Vecteur_lat = []
    for row in TasksDico:
        Vecteur_lat.append(row['Latitude'])
    return Vecteur_lat


# tri de list_to_order par ordre décroissant sur la list_used_for_order
def order_list(list_to_order, list_used_for_order):
    if len(list_used_for_order) != len(list_to_order):
        return "Erreur : les listes à trier ne sont pas de la même dimension"
    list_used_for_order_2 = list_used_for_order.copy()
    order = [i for i in range(len(list_used_for_order_2))]
    i = 0
    while i < len(list_used_for_order_2) - 1:
        if list_used_for_order_2[i] > list_used_for_order_2[i+1]:
            list_used_for_order_2[i], list_used_for_order_2[i +
                                                            1] = list_used_for_order_2[i+1], list_used_for_order_2[i]
            order[i], order[i+1] = order[i+1], order[i]
            i = -1
        i = i + 1

    list_to_order_2 = [list_to_order[indice] for indice in order]

    return list_to_order_2


def creation_listes(longitudes, lattitudes, employes, taches, start_times, nom_ville):
    path="Phase_1/InstancesV1/Instance"+str(nom_ville)+"V1.xlsx"
    EmployeesDico, TasksDico = extraction_data(path)
    
    employes_unique = []
    #Liste des employés qui ne comporte qu'une fois chacun
    for employe in employes:
        if employe not in employes_unique:
            employes_unique += [employe]

    listesPlot=[]
    #cette liste contient : [employe[longitudes[l1l2l3],latitudes[m1m2m3]]]
    for i in range(len(employes_unique)):
        #on extrait les longitudes et latitudes des tâches effectuées par l'employé i
        longitudes_employe = [longitudes[j] for j in range(
            len(employes)) if employes[j] == employes_unique[i]]
        lattitudes_employe = [lattitudes[j] for j in range(
            len(employes)) if employes[j] == employes_unique[i]]

        start_times_employe = [start_times[j] for j in range(
            len(employes)) if employes[j] == employes_unique[i]]

        # On trie les longitudes/lattitudes des tâches des employés par ordre croissant de début de leurs tâches

        lattitudes_employe = order_list(
            lattitudes_employe, start_times_employe)
        longitudes_employe = order_list(
            longitudes_employe, start_times_employe)

        # Ajout des domiciles des employés
        found_name=False
        j=0
        while not found_name and j<len(EmployeesDico):
            if employes_unique[i]==EmployeesDico[j]['EmployeeName']:
                found_name=True
                longitude_domicile_i=EmployeesDico[j]['Longitude']
                latitude_domicile_i=EmployeesDico[j]['Latitude']
            j+=1
        longitudes_employe.insert(0, longitude_domicile_i)
        lattitudes_employe.insert(0, latitude_domicile_i)
        longitudes_employe += [longitude_domicile_i]
        lattitudes_employe += [latitude_domicile_i]

        listesPlot.append([longitudes_employe,lattitudes_employe])
    return listesPlot

def graphiquePyplot(longitudes, lattitudes, employes, taches, start_times, nom_ville):
    listesPlot=creation_listes(longitudes, lattitudes, employes, taches, start_times, nom_ville)

    my_colors = ["r", "g", "b", "c", "m", "y",
                 "k", "r", "g", "b", "c", "m", "y", "k"]

    employes_unique = []
    #Liste des employés qui ne comporte qu'une fois chacun
    for employe in employes:
        if employe not in employes_unique:
            employes_unique += [employe]

    for i in range(len(listesPlot)):
        plt.plot(listesPlot[i][0],listesPlot[i][1],
                 "-o", color=my_colors[i], label=str(employes_unique[i]))
        for j in range(len(employes)):
            if employes[j] == employes_unique[i]:
                plt.annotate(str(taches[j]),
                             (longitudes[j], lattitudes[j]))

    plt.title(str(nom_ville))
    plt.legend()
    plt.show()
    return None


# longitudes, lattitudes = extraire_coordonnees(path='InstanceBordeauxV1.xlsx')


# affichage_graphique(longitudes, lattitudes, lecture("SolutionBordeauxV1ByV1.txt")[
#                     0], lecture("SolutionBordeauxV1ByV1.txt")[1])


def afficher(nom_ville):
    path1 = "Phase_1/InstancesV1/Instance"+str(nom_ville)+"V1.xlsx"
    path2 = "Phase_1/Solutions/Solution"+str(nom_ville)+"V1ByV1.txt"

    longitudes, lattitudes, long_employe, latt_employe = extraire_coordonnees(
        nom_ville)
    employes, taches, start_times = lecture(path2)

    graphiquePyplot(longitudes, lattitudes, employes, taches, start_times, nom_ville)

    my_colors = ["r", "g", "b", "c", "m", "y", "k", "r", "g", "b", "c", "m", "y", "k"]

    listesPlot=creation_listes(longitudes, lattitudes, employes, taches, start_times, nom_ville)
    m = folium.Map(location=[lattitudes[0],longitudes[0]],zoom_start=15)
    for i in range (len(listesPlot)):
        loc = []
        for j in range(len(listesPlot[i][0])):
            loc.append((listesPlot[i][0][j],listesPlot[i][1][j]))
            print(loc)
    folium.PolyLine(loc,color='red',weight=2,opacity=0.8).add_to(m)
    print('i added')

    m.save("testfolium.html")
    return None

afficher('Bordeaux')


