
from cmath import inf
from msilib.schema import Error
import numpy as np
from sympy import solve
import math
import pandas as pd

def getsol(path):
    '''construit un dictionnaire correspondant à une solution à partir d'un excel
    '''
    Tab = np.array(pd.read_excel(path, names=['Employé',	'TaskId',	'precedent',	'suivant',	'heure']))
    S = {}
    for i in range(len(Tab)):
        name = Tab[i,0]
        Taskid = Tab[i,1]
        precedent = Tab[i,2]
        suivant = Tab[i,3]
        heure =Tab[i,4]
        if name in S.keys():
            S[name][Taskid] = {"precedent":precedent, "suivant":suivant, "heure":heure}
        else :
             S[name] = {Taskid:{"precedent":precedent, "suivant":suivant, "heure":heure}}
    return S


def extractionData(path):
    """Permet l'extraction des données depuis un fichier excel.
    path est une chaîne de caratères correspondant à l'emplacement relatif du fichier.
    Renvoie les différents dictionnaires permettant un traitement des données avec python."""
    xls = pd.ExcelFile(path)
    df1 = pd.read_excel(xls, 'Employees')
    df2 = pd.read_excel(xls, 'Employees Unavailabilities')
    df3 = pd.read_excel(xls, 'Tasks')
    df4 = pd.read_excel(xls, 'Tasks Unavailabilities')

    # Création des dictionnaires de données
    EmployeesDico = df1.to_dict('records')
    EmployeesUnavailDico = df2.to_dict('records')
    TasksDico = df3.to_dict('records')
    TasksUnavailDico = df4.to_dict('records')

    return EmployeesDico, EmployeesUnavailDico, TasksDico, TasksUnavailDico


# Fonctions utiles pour créer les matrices de données utiles

def deg2rad(dd):
    """Convertit un angle "degrés décimaux" en "radians"
    """
    return dd/180*math.pi

def distanceGPS(latA, longA, latB, longB):
    """Retourne la distance en mètres entre les 2 points A et B connus grâce à
       leurs coordonnées GPS (en radians).
    """
    # Rayon de la terre en mètres (sphère IAG-GRS80)
    RT = 6378137
    # angle en radians entre les 2 points
    x = math.sin(latA)*math.sin(latB) + math.cos(latA)*math.cos(latB)*math.cos(abs(longB-longA))        
    if abs(x-1) <= 0.000000000001:
        x = 1
    elif abs(x+1) <= 0.000000000001:
        x = -1
    S = math.acos(x)
    # distance entre les 2 points, comptée sur un arc de grand cercle
    return S*RT
    
def distance(id1, id2, TasksDico):
    """Calcule la distance entre deux points dont on connait les coordonnées GPS.
    Entrée : les taskid correspondantes et le dictionnaire de données.
    Sortie : distance en km."""
    foundId1, foundId2 = False, False
    index = 0
    while not (foundId1 and foundId2):
        if TasksDico[index]['TaskId'] == id1:
            foundId1 = True
            long1 = deg2rad(TasksDico[index]['Longitude'])
            lat1 = deg2rad(TasksDico[index]['Latitude'])
        if TasksDico[index]['TaskId'] == id2:
            foundId2 = True
            long2 = deg2rad(TasksDico[index]['Longitude'])
            lat2 = deg2rad(TasksDico[index]['Latitude'])
        index += 1

    #distance d'arc entre deux points
    distance = round(distanceGPS(lat1,long1,lat2,long2)/1000,1)
    return distance


def competenceOK(EmployeeName, TaskId, TasksDico, EmployeesDico):
    """EmployeeName est une chaîne de caractères correspondant au nom d'un employé.
    TaskId est l'identifiant d'une tâche.
    TasksDico et EmployeesDico sont les dictionnaires contenant les informations respectives sur les tâches et les employés.
    Retourne 1 si l'employé a la bonne compétence et un niveau suffisant pour effectuer la tâche, 0 sinon."""
    taskSkill = next(item['Skill']
                     for item in TasksDico if item['TaskId'] == TaskId)
    employeeSkill = next(
        item['Skill'] for item in EmployeesDico if item['EmployeeName'] == EmployeeName)
    taskLevel = next(item['Level']
                     for item in TasksDico if item['TaskId'] == TaskId)
    employeeLevel = next(
        item['Level'] for item in EmployeesDico if item['EmployeeName'] == EmployeeName)
    if taskLevel <= employeeLevel and taskSkill == employeeSkill:
        return 1
    elif taskSkill == None:
        return 1
    else:
        return 0


# Fonctions création des matrices nécessaires au calcul de la fonction coût et à la vérification des contraintes

def matriceDistance(TasksDico):
    """TasksDico est le dictionnaire contenant les informations sur les tâches.
    Renvoie la matrice des distances entre les différentes tâches."""
    matriceDesDistances = []
    for tache1 in TasksDico:
        taskId1 = tache1["TaskId"]
        ligne = []
        for tache2 in TasksDico:
            taskId2 = tache2["TaskId"]
            ligne.append(distance(taskId1, taskId2, TasksDico))
        matriceDesDistances.append(ligne)
    return matriceDesDistances


def matriceCompetences(EmployeesDico, TasksDico):
    """TasksDico et EmployeesDico sont les dictionnaires contenant les informations respectives sur les tâches et les employés.
    Renvoie une matrice C qui comporte un 1 si l'employé n peut faire la tache i et un 0 sinon."""
    nombreEmployes = len(EmployeesDico)
    nombreTaches = len(TasksDico)
    C = np.zeros((nombreEmployes, nombreTaches))
    for n in range(nombreEmployes):
        for i in range(nombreTaches):
            C[n, i] = competenceOK(
                EmployeesDico[n]['EmployeeName'], TasksDico[i]['TaskId'], TasksDico, EmployeesDico)
    return C


# Fonctions récupération des contraintes temporelles des tâches

def recuperationHeure(heure):
    """heure est une chaîne de caractères de la forme 11:15pm.
    Renvoie un entier correspondant au nombre de minutes écoulées depuis minuit."""
    res = heure.split(':')
    h = int(res[0])  # l'heure
    m = int(res[1][:2])  # les minutes
    if res[1][2:] == 'pm':
        if res[0] != 12:
            h += 12  # modifications pour l'aprem
    else:
        if res[0] == 12:
            h = 0
    return h*60+m


def vecteurOuvertures(TasksDico, TasksUnavailDico):
    """TasksDico et TasksUnavailDico sont les dictionnaires contenant les informations respectives sur les tâches et leurs indisponibilités.
    Renvoie une liste de liste avec les heures d'ouvertures de chaque tâche après chaque indisponibilité."""
    nombreTaches = len(TasksDico)
    nombreIndisponibilite = len(TasksUnavailDico)
    O = []
    for i in range(nombreTaches):
        horairesOvertures = []
        heure = TasksDico[i]['OpeningTime']
        horairesOvertures.append(recuperationHeure(heure))
        for k in range(nombreIndisponibilite):
            # on vérifie que l'indisponibilité correspond à la tâche i
            if TasksDico[i]['TaskId'] == TasksUnavailDico[k]['TaskId']:
                heure = TasksUnavailDico[k]['End']
                # ajout de l'heure de réouverture après l'indisponibilité k de la tâche i
                horairesOvertures.append(recuperationHeure(heure))
        O.append(horairesOvertures)
    return O


def vecteurFermetures(TasksDico, TasksUnavailDico):
    """TasksDico et TasksUnavailDico sont les dictionnaires contenant les informations respectives sur les tâches et leurs indisponibilités.
    Renvoie une liste de liste avec les heures de fermetures de chaque tâche avant chaque indisponibilité."""
    nombreTaches = len(TasksDico)
    nombreIndisponibilites = len(TasksUnavailDico)
    F = []
    for i in range(nombreTaches):
        horairesFermetures = []
        heure = TasksDico[i]['ClosingTime']
        horairesFermetures.append(recuperationHeure(heure))
        for k in range(nombreIndisponibilites):
            # on vérifie que l'indisponibilité correspond à la tâche i
            if TasksDico[i]['TaskId'] == TasksUnavailDico[k]['TaskId']:
                heure = TasksUnavailDico[k]['Start']
                # ajout de l'heure de réouverture après l'indisponibilité k de la tâche i
                horairesFermetures.append(recuperationHeure(heure))
        F.append(horairesFermetures)
    return F


def vecteurDurees(TasksDico):
    """TasksDico est le dictionnaire contenant les informations sur les tâches.
    Renvoie le vecteur des durées de chaque tâche."""
    Vecteur = []
    for row in TasksDico:
        Vecteur.append(row['TaskDuration'])
    return Vecteur


def estDansUnCreneau(heure,creneau):
    n = len(creneau)
    for j in range(n):
        if creneau[j][0] <= heure <= creneau[j][1] :
            return True
    return False


def getCreneaux(heure,creneauxTache):
    """Cette fonction renvoie l'heure de début et l'heure de fin du crénaux de disponibilité contenant l'heure donnée"""
    n = len(creneauxTache)
    for j in range(n):
        if creneauxTache[j][0] <= heure <= creneauxTache[j][1] :
            return creneauxTache[j][0], creneauxTache[j][1]


def MAJTempsSuivants(i0,solution_k,creneauxDispo_k,Duree,D):
    solution_k = solution_k.copy()
    """Cette fonction permet de contracter les temps en aval d'une tache i0. Autrement dit elle tasse les heures en fin de journée à partir d'une tache i0 incluse"""
    iCourant = 0
    precedentCourant = solution_k[iCourant]["precedent"]
    h = int(18*60 - D[precedentCourant,iCourant]/0.833)
    while iCourant != i0 : # tant qu'on arrive pas à la maison
        # On regarde si la tache d'après peut être faite avant l'heure prévu tout en restant dans le crénaux de dispo
        hmin,hmax = getCreneaux(solution_k[precedentCourant]["heure"],creneauxDispo_k[precedentCourant])
        if hmin + Duree[precedentCourant] <= h <= hmax :
            solution_k[precedentCourant]["heure"] = int(h - Duree[precedentCourant])
        elif h > hmax :
            solution_k[precedentCourant]["heure"] = int(hmax - Duree[precedentCourant])
        else:
            print("Error") 
        iCourant = precedentCourant
        precedentCourant = solution_k[iCourant]["precedent"]
        h = int(solution_k[iCourant]["heure"] - D[precedentCourant,iCourant]/0.833)
    return solution_k


def MAJTempsPrecedents(i0,solution_k,creneauxDispo_k,Duree,D):
    solution_k = solution_k.copy()
    """Cette fonction permet de contracter les temps en amont d'une tache i0. Autrement dit elle tasse les heures en début de journée à partir d'une tache i0 incluse"""
    iCourant = 0
    suivantCourant = solution_k[iCourant]["suivant"]
    while iCourant != i0: # tant qu'on arrive pas à la maison
        # On regarde si la tache d'après peut être faite avant l'heure prévu tout en restant dans le crénaux de dispo
        h = int(solution_k[iCourant]["heure"] + Duree[iCourant] + D[iCourant,suivantCourant]/0.833)
        hmin,hmax = getCreneaux(solution_k[suivantCourant]["heure"],creneauxDispo_k[suivantCourant])
        if hmin <= h <= hmax :
            solution_k[suivantCourant]["heure"] = h
        elif h < hmin :
            solution_k[suivantCourant]["heure"] = h
        else:
            print("Error") 
        iCourant = suivantCourant
        suivantCourant = solution_k[iCourant]["suivant"]
    return solution_k


def insertionTache(i,precedent,suivant,solution_k,creneauxDispoTaches,Duree,D):
    solution_k = solution_k.copy()
    solution_k = MAJTempsPrecedents(precedent,solution_k,creneauxDispoTaches,Duree,D)
    solution_k = MAJTempsSuivants(suivant,solution_k,creneauxDispoTaches,Duree,D)
    solution_k[precedent]["suivant"] = i
    solution_k[suivant]["precedent"] = i
    solution_k[i] = {"precedent":precedent, "suivant":suivant}
    h = solution_k[precedent]["heure"] + Duree[precedent] + D[precedent,i]/0.833
    if estDansUnCreneau(h,creneauxDispoTaches[i]):
        solution_k[i]["heure"] = int(h)
    else:
        L = [creneauxDispoTaches[i][j][0] for j in range(len(creneauxDispoTaches[i]))].sort()
        for hmin in L:
            found = 0
            if h < hmin and found == 0:
                found = 1
                solution_k[i]["heure"] = int(hmin)
    if solution_k[i]["heure"] + Duree[i] + D[i,suivant]/0.833 > solution_k[suivant]["heure"]:
        print("insertion impossible")
        return None
    return solution_k

def suppressionTache(i,solution_k):
    solution_k = solution_k.copy()
    precedent = solution_k[i]["precedent"]
    suivant = solution_k[i]["suivant"]
    solution_k[precedent]["suivant"] = suivant
    solution_k[suivant]["precedent"] = precedent
    del solution_k[i]
    return solution_k


        



sol_test = {0:{"precedent" : 2, "suivant" : 3, "heure": 8*60}, 1:{"precedent" : 3, "suivant" : 2, "heure" : 8.5*60}, 2:{"precedent" : 1, "suivant" : 0, "heure" : 11*60}, 3:{"precedent" : 0, "suivant" : 1, "heure" : 10*60}}
sol2 = sol_test.copy()
creneauxDispo_test = [[[8*60,12*60],[13*60,18*60]]]*5
Duree = 30*np.ones((5,1))
D = np.array([[0, 2, 5, 1, 10],
              [2, 0, 4, 3, 6],
              [5, 4, 0, 6, 8],
              [1, 3, 6, 0, 11],
              [12, 3, 7, 8, 0]])
i0 = 3
tGlande = np.NaN*np.zeros((4,4))

sol_test = insertionTache(4,3,1,sol_test,creneauxDispo_test,Duree,D)
print(sol_test)
print(suppressionTache(1,sol_test))
print(sol2)


# pour prendre en compte la pause dej en mettant une indispo employé à lieu non fixé none
