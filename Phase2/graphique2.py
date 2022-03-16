import matplotlib.pyplot as plt
from usefulFunctions2 import extractionData
import folium



def lecture(filename):
    '''entrée : nom du fichier solution, sortie : les vecteurs employes (noms), taches (numeros), start_times (minutes)'''
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


# Fonctions auxiliaires
# Vecteur des longitudes
# Nécessitent de revenir à la liste des tâches, qui comporte les localisations
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

def extraire_coordonnees(nom_ville):
    '''entrée : nom de la ville, sortie : longitudes et latitudes des taches  dans l'ordre de leur ID'''
    path="Phase2/InstancesV2/Instance"+str(nom_ville)+"V2.xlsx"
    EmployeesDico, _,TasksDico,_ = extractionData(path)
    return vecteur_longitudes(TasksDico), vecteur_latitudes(TasksDico),

# tri de list_to_order par ordre décroissant sur la list_used_for_order
def order_list(list_to_order, list_used_for_order):
    '''Fonction auxiliaire'''
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


def creation_listes(nom_ville):
    path="Phase2/InstancesV2/Instance"+str(nom_ville)+"V2.xlsx"
    EmployeesDico, _,TasksDico,_= extractionData(path)
    
    filename= "Phase2/Solutions/Solution"+str(nom_ville)+"V2ByV2.txt"
    employes, taches, start_times= lecture(filename)

    longitudes_taches, latitudes_taches = extraire_coordonnees(nom_ville)
    employes_unique = []
    #Liste des employés qui ne comporte qu'une fois chacun
    for employe in employes:
        if employe not in employes_unique and employe!='':
            employes_unique += [employe]

    listesPlot=[]
    #cette liste contient : [employe[longitudes[l1l2l3],latitudes[m1m2m3]]]
    for i in range(len(employes_unique)):
        #on extrait les longitudes et latitudes des tâches effectuées par l'employé i
        longitudes_i=[]
        lattitudes_i=[]
        start_times_i=[]
        for j in range (len(employes)):
            id_tache=int(taches[j][1:])-1
            # les taches sont dans l'ordre normal... pas dans l'ordre de sortie de lecture c'est le meme patatoide. Donc on doit relier la ligne j au numéro de la tâche
            if employes[j]==employes_unique[i]:
                print(taches[j])
                print(id_tache)
                longitudes_i.append(longitudes_taches[id_tache])
                lattitudes_i.append(latitudes_taches[id_tache])
                start_times_i.append(start_times[j])

        # On trie les longitudes/lattitudes des tâches des employés par ordre croissant de début de leurs tâches

        lattitudes_i = order_list(
            lattitudes_i, start_times_i)
        longitudes_i = order_list(
            longitudes_i, start_times_i)

        # Ajout des domiciles des employés
        found_name=False
        j=0
        while not found_name and j<len(EmployeesDico):
            if employes_unique[i]==EmployeesDico[j]['EmployeeName']:
                found_name=True
                longitude_domicile_i=EmployeesDico[j]['Longitude']
                latitude_domicile_i=EmployeesDico[j]['Latitude']
            j+=1
        longitudes_i.insert(0, longitude_domicile_i)
        lattitudes_i.insert(0, latitude_domicile_i)
        longitudes_i += [longitude_domicile_i]
        lattitudes_i += [latitude_domicile_i]

        listesPlot.append([longitudes_i,lattitudes_i])
    return listesPlot

def graphiquePyplot(longitudes, lattitudes, employes, taches, nom_ville):
    listesPlot=creation_listes(nom_ville)

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


def afficher(nom_ville):
    path1 = "Phase2/InstancesV2/Instance"+str(nom_ville)+"V2.xlsx"
    path2 = "Phase2/Solutions/Solution"+str(nom_ville)+"V2ByV2.txt"

    longitudes, lattitudes = extraire_coordonnees(
        nom_ville)
    employes, taches, start_times = lecture(path2)

    graphiquePyplot(longitudes, lattitudes, employes, taches, nom_ville)

    my_colors = ["r", "g", "b", "c", "m", "y", "k", "r", "g", "b", "c", "m", "y", "k"]

    listesPlot=creation_listes(nom_ville)
    m = folium.Map(location=[lattitudes[0],longitudes[0]],zoom_start=15)
    for i in range (len(listesPlot)):
        loc = []
        for j in range(len(listesPlot[i][0])):
            loc.append((listesPlot[i][0][j],listesPlot[i][1][j]))
            print(loc)
        folium.PolyLine(loc,color='red',weight=2,opacity=0.8).add_to(m)

    m.save("testfolium.html")
    return None

afficher('Australia')


