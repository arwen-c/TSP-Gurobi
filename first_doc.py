## Premère mission : extraire du CSV

from cmath import cos
from math import dist
from numpy import real
import pandas as pd


xls = pd.ExcelFile('InstanceFinlandV1.xlsx')
df1 = pd.read_excel(xls, 'Employees')
df2 = pd.read_excel(xls, 'Tasks')

## Deuxième mission : créer des dictionnaires de données
EmployeesDico = df1.to_dict('records')
TasksDico = df2.to_dict('records')
#print (TasksDico)

import math

def distance(id1,id2): 
    '''entrée : les taskid correspondantes, sortie : distance en km'''
    foundid1, foundid2=False,False
    index=0
    while not (foundid1 and foundid2):
        if TasksDico[index]['TaskId']==id1:
            foundid1=True
            long1=TasksDico[index]['Longitude']
            lat1=TasksDico[index]['Latitude']
        if TasksDico[index]['TaskId']==id2:
            foundid2=True
            long2=TasksDico[index]['Longitude']
            lat2=TasksDico[index]['Latitude']
        index+=1
    delta_long = long2-long1
    delta_latt = lat2-lat1
    d=(1.852*60*math.sqrt(delta_long**2+delta_latt**2))
    return d

#print (distance('T18','T24'))

def temps_trajet(id1,id2):
    '''Calcul du temps de trajet entre deux tâches, en heures'''
    return distance(id1,id2)/50
