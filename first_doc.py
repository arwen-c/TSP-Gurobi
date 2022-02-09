## Premère mission : extraire du CSV

from math import dist
import pandas as pd
xls = pd.ExcelFile('ST transport\InstanceFinlandV1.xlsx')
df1 = pd.read_excel(xls, 'Employees')
df2 = pd.read_excel(xls, 'Tasks')

## Deuxième mission : créer des dictionnaires de données
EmployeesDico = df1.to_dict('records')
TasksDico = df2.to_dict('records')
#print (TasksDico)

##Calcul de distance entre deux tâches
def distance(id1,id2): #entrée : les taskid correspondantes
    foundid1, foundid2=False,False
    index=0
    while not foundid1 and foundid2:
        if TasksDico[index]['TaskId']==id1:
            foundid1=True
            long1=TasksDico[index]['Longitude']
            lat1=TasksDico[index]['Latitude']
        if TasksDico[index]['TaskId']==id2:
            foundid2=True
            long2=TasksDico[index]['Longitude']
            lat2=TasksDico[index]['Latitude']
        index+=1
    return dist([long1,lat1],[long2,lat2])


