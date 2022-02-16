# Premère mission : extraire du CSV

from cmath import cos
from math import dist
import numpy as np
import pandas as pd
import math


xls = pd.ExcelFile('InstanceFinlandV1.xlsx')
df1 = pd.read_excel(xls, 'Employees')
df2 = pd.read_excel(xls, 'Tasks')

# Deuxième mission : créer des dictionnaires de données
EmployeesDico = df1.to_dict('records')
TasksDico = df2.to_dict('records')
#print (EmployeesDico)f


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


def matrice_distance(dic_taches):
    x = len(dic_taches)
    matrice_des_distances = np.zeros(x, x)
    for id1 in dic_taches:
        chaine_carac_id1 = str(id1)
        i = int(chaine_carac_id1[1:])
        for id2 in dic_taches:
            chaine_carac_id2 = str(id2)
            j = int(chaine_carac_id2[1:])
            matrice_des_distances[i, j] = distance(id1, id2)
    return matrice_des_distances
    
def matriceCompetences():
    '''Crée une matrice C_ni qui comporte un 1 si l'employé n peut faire la tache i'''
    nombre_employes=len(EmployeesDico)
    nombre_taches=len(TasksDico)
    C=np.zeros((nombre_employes,nombre_taches))
    for n in range(nombre_employes) :
        for i in range(nombre_taches):
            C[n,i]=competenceOK(EmployeesDico[n]['EmployeeName'],TasksDico[i]['TaskId'])
    return C

def vecteurOuvertures():
    '''Crée un vecteur avec les heures d'ouvertures des tâches'''
    nombre_taches=len(TasksDico)
    O=[]
    for i in range(nombre_taches):
        heure=TasksDico[i]['OpeningTime']
        res=heure.split(':')
        h=int(res[0]) #l'heure
        m=int(res[1][:1]) #les minutes
        if res[1][2:]=='pm':
            h+=12 #modifications pour l'aprem
        O.append(h*60+m)
    return O

def vecteurFermetures():
    '''Crée un vecteur avec les heures de fermeture des tâches'''
    nombre_taches=len(TasksDico)
    F=[]
    for i in range(nombre_taches):
        heure=TasksDico[i]['ClosingTime']
        res=heure.split(':')
        h=int(res[0]) #l'heure
        m=int(res[1][:1]) #les minutes
        if res[1][2:]=='pm':
            h+=12 #modifications pour l'aprem
        F.append(h*60+m)
    return F