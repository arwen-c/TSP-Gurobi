# Premère mission : extraire du CSV

from asyncio import Task
from cmath import cos
from math import dist
import numpy as np
import pandas as pd
import math

fichier_test = 'InstanceFinlandV1.xlsx'

xls = pd.ExcelFile(fichier_test)
df1 = pd.read_excel(xls, 'Employees')
df2 = pd.read_excel(xls, 'Tasks')

# Deuxième mission : créer des dictionnaires de données
EmployeesDico = df1.to_dict('records')
TasksDico = df2.to_dict('records')
# print (EmployeesDico)f


def distance(id1, id2):
    '''entrée : les taskid correspondantes, sortie : distance en km'''
    foundid1, foundid2 = False, False
    index = 0
    while not (foundid1 and foundid2):
        if TasksDico[index]['TaskId'] == id1:
            foundid1 = True
            long1 = TasksDico[index]['Longitude']
            lat1 = TasksDico[index]['Latitude']
        if TasksDico[index]['TaskId'] == id2:
            foundid2 = True
            long2 = TasksDico[index]['Longitude']
            lat2 = TasksDico[index]['Latitude']
        index += 1
    delta_long = long2-long1
    delta_latt = lat2-lat1
    d = (1.852*60*math.sqrt(delta_long**2+delta_latt**2))
    return d


def temps_trajet(id1, id2):
    '''Calcul du temps de trajet entre deux tâches, en minutes'''
    return distance(id1, id2)*60/50


def competenceOK(EmployeeName, TaskId):
    '''Retourne 1 si l'employé a le bon skill et un niveau suffisant pour effectuer la tâche'''
    task_skill = next(item['Skill']
                      for item in TasksDico if item['TaskId'] == TaskId)
    employee_skill = next(
        item['Skill'] for item in EmployeesDico if item['EmployeeName'] == EmployeeName)
    task_level = next(item['Level']
                      for item in TasksDico if item['TaskId'] == TaskId)
    employee_level = next(
        item['Level'] for item in EmployeesDico if item['EmployeeName'] == EmployeeName)
    if task_level <= employee_level and task_skill == employee_skill:
        return 1
    else:
        return 0


<<<<<<< HEAD
def matrice_distance(dic_taches):
    x = len(dic_taches)
    matrice_des_distances = np.zeros((x, x))
    for tache_1 in dic_taches :
        task_id_1 = tache_1["TaskId"]
        i = int(task_id_1[1:])
        for tache_2 in dic_taches[i:]:
            task_id_2 = tache_2["TaskId"]
            j = int(task_id_2[1:])
            print(task_id_1, task_id_2)
            matrice_des_distances[i-1, j-1] = distance(task_id_1, task_id_2)
<<<<<<< HEAD
    return matrice_des_distances
=======
            matrice_des_distances[j-1, i-1] = distance(task_id_1, task_id_2)
>>>>>>> PACh

    return matrice_des_distances


def matrice_temps_de_trajet(D): # prend en entré un tableau des distances D
    return D/(50/60) # il se déplace à 50km/h donc 50/60 km/min

<<<<<<< HEAD
print(TasksDico[0])

print(matrice_temps_de_trajet(matrice_distance(TasksDico)))
=======
def matrice_distance():
    x = len(TasksDico)
    matrice_des_distances = np.zeros((x, x))
    for id1 in TasksDico:
        chaine_carac_id1 = str(id1)
        i = int(chaine_carac_id1[1:])
        for id2 in TasksDico:
            chaine_carac_id2 = str(id2)
            j = int(chaine_carac_id2[1:])
            matrice_des_distances[i, j] = distance(id1, id2)
    return matrice_des_distances


=======
    
>>>>>>> PACh
def matriceCompetences():
    '''Crée une matrice C_ni qui comporte un 1 si l'employé n peut faire la tache i'''
    nombre_employes = len(EmployeesDico)
    nombre_taches = len(TasksDico)
    C = np.zeros((nombre_employes, nombre_taches))
    for n in range(nombre_employes):
        for i in range(nombre_taches):
            C[n, i] = competenceOK(
                EmployeesDico[n]['EmployeeName'], TasksDico[i]['TaskId'])
    return C


def vecteurOuvertures():
    '''Crée un vecteur avec les heures d'ouvertures des tâches'''
    nombre_taches = len(TasksDico)
    O = []
    for i in range(nombre_taches):
        heure = TasksDico[i]['OpeningTime']
        res = heure.split(':')
        h = int(res[0])  # l'heure
        m = int(res[1][:1])  # les minutes
        if res[1][2:] == 'pm':
            h += 12  # modifications pour l'aprem
        O.append(h*60+m)
    return O


def vecteurFermetures():
    '''Crée un vecteur avec les heures de fermeture des tâches'''
    nombre_taches = len(TasksDico)
    F = []
    for i in range(nombre_taches):
        heure = TasksDico[i]['ClosingTime']
        res = heure.split(':')
        h = int(res[0])  # l'heure
        m = int(res[1][:1])  # les minutes
        if res[1][2:] == 'pm':
            h += 12  # modifications pour l'aprem
        F.append(h*60+m)
    return F
<<<<<<< HEAD


def vecteur_duree_tache():
    """Pas besoin d'argument, on utilise les variables globales.
    Renvoie le vecteur des durées de chaque tâche."""
    x = len(TasksDico)
    Vecteur_duree = np.zeros((x, x))
    for k in range(x):
        Vecteur_duree[int(TasksDico[k]['TaskId'][1:])
                      ] = TasksDico[k]['TaskDuration']
    return Vecteur_duree


# Création du fichier solution


def nom_fichier_resolution(nom_fichier, n_methode):
    """nom_fichier est un string qui correspond au nom du fichier excel.
    n_methode est le numéro de la méthode.
    Renvoie le nom du fichier txt."""
    L = nom_fichier.split('.')
    return 'Solution' + L[0][9:] + 'ByV' + 'n_methode'+'.txt'


def solution_fichier_txt(X, h):
    """X et h sont des tableaux numpy. 
    X est de dimension 3 et h de dimension 1.
    Renvoie la liste des lignes sous la forme souhaitée pour le fichier .txt."""
    premiere_ligne = 'taskId;performed;employeeName;startTime;'
    liste_des_lignes = [premiere_ligne]
    n, x, y = X.shape()
    employeeName = ''
    for i in range(x):
        j = 0
        tache_i_ajoutee = False
        while j < y and not(tache_i_ajoutee):
            numero_employe = 0
            while numero_employe < n and not(tache_i_ajoutee):
                if X[numero_employe, i, j] == 1:
                    employeeName = EmployeesDico[numero_employe]['EmployeeName']
                    liste_des_lignes.append(
                        'T' + str(i) + ';' + '1' + employeeName + ';' + h[i])
                    tache_i_ajoutee = True
                numero_employe = numero_employe + 1
            j = j + 1
        if not(tache_i_ajoutee):
            liste_des_lignes.append(
                'T' + str(i) + ';' + '0' + 'None' + ';' + 'None')
    return liste_des_lignes


def creation_fichier(nom_fichier, n_methode, X, h):
    """nom_fichier est le nom du fichier utilisée pour créer les variables globales.
    n_methode est le numéro de la méthode utilisée.
    X est un tableau en 3 dimensions où chaque coefficient permet de savoir si l'employé n est allé de la tâche i à la tâche j.
    Ne renvoie rien mais crée ou modifie le fichier .txt."""
    file = open(nom_fichier_resolution(fichier_test, 1), "w")
    file.write("\n".join(solution_fichier_txt(X, h)))
    file.close()
    return None
>>>>>>> e9935c3c61bb3d434241984be79c6e13c34fd876
=======
>>>>>>> PACh
