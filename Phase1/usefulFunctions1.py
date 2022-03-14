# Import de modules
import numpy as np
import pandas as pd
import math


# Fonction récupération des données issues des excel


def extractionData(path):
    """Permet l'extraction des données depuis un fichier excel.
    path est une chaîne de caratères correspondant à l'emplacement relatif du fichier.
    Renvoie les différents dictionnaires permettant un traitement des données avec python."""
    xls = pd.ExcelFile(path)
    df1 = pd.read_excel(xls, 'Employees')
    df2 = pd.read_excel(xls, 'Tasks')

    # Création des dictionnaires de données
    EmployeesDico = df1.to_dict('records')
    TasksDico = df2.to_dict('records')

    return EmployeesDico, TasksDico


# Fonctions utiles pour créer les matrices de données utiles

def distance(id1, id2, TasksDico):
    """Calcule la distance entre deux points dont on connait les coordonnées GPS.
    Entrée : les taskid correspondantes et le dictionnaire de données.
    Sortie : distance en km."""
    foundId1, foundId2 = False, False
    index = 0
    while not (foundId1 and foundId2) and index < len(TasksDico):
        if TasksDico[index]['TaskId'] == id1:
            foundId1 = True
            long1 = TasksDico[index]['Longitude']
            lat1 = TasksDico[index]['Latitude']
        if TasksDico[index]['TaskId'] == id2:
            foundId2 = True
            long2 = TasksDico[index]['Longitude']
            lat2 = TasksDico[index]['Latitude']
        index += 1
    if long1 is None or long2 is None:
        distance = 0
    else:
        delta_long = long2-long1  # calcule de la différence de longitude
        delta_latt = lat2-lat1
        distance = (1.852*60*math.sqrt(delta_long**2+delta_latt**2))
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


def vecteurOuvertures(TasksDico):
    """TasksDico est le dictionnaire contenant les informations respectives sur les tâches.
    Renvoie une liste avec l'heure d'ouverture de chaque tâche."""
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


def vecteurFermetures(TasksDico):
    """TasksDico est le dictionnaire contenant les informations respectives sur les tâches.
    Renvoie une liste avec l'heure de fermeture de chaque tâche."""
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


def vecteurDurees(TasksDico):
    """TasksDico est le dictionnaire contenant les informations sur les tâches.
    Renvoie le vecteur des durées de chaque tâche."""
    Vecteur_duree = []
    for row in TasksDico:
        Vecteur_duree.append(row['TaskDuration'])
    return Vecteur_duree


# Création du fichier solution


def nomFichierResolution(nomFichier, nMethode):
    """nom_fichier est un string qui correspond au nom du fichier excel.
    n_methode est le numéro de la méthode.
    Renvoie le nom du fichier txt."""
    L = nomFichier.split('.')
    nMethode = str(nMethode)
    # return 'Solution' + L[0][8:] + 'ByV' + n_methode + '.txt' # ancienne version sans arborescence pour les fichiers excels
    # nouvelle version avec arborescence pour les fichiers excels
    return 'Phase1/Solutions/Solution' + L[0][28:] + 'ByV' + nMethode + '.txt'


def lignesSolution(X, h, EmployeesDico):
    """X et h sont des tableaux numpy.
    X est de dimension 3 et h de dimension 1.
    Renvoie la liste des lignes sous la forme souhaitée pour le fichier .txt."""
    premiereLigne = 'taskId;performed;employeeName;startTime;'
    listeDesLignes = [premiereLigne]
    n, x, y = X.shape
    employeeName = ''
    for i in range(x - 2*n):
        j = 0
        tacheiAjoutee = False
        while j < y and not(tacheiAjoutee):
            numeroEmploye = 0
            while numeroEmploye < n and not(tacheiAjoutee):
                if X[numeroEmploye, i, j] == 1:
                    employeeName = EmployeesDico[numeroEmploye]['EmployeeName']
                    listeDesLignes.append(
                        'T' + str(i+1) + ';' + '1' + ';' + str(employeeName) + ';' + str(round(h[i])) + ';')
                    tacheiAjoutee = True
                numeroEmploye = numeroEmploye + 1
            j = j + 1
        if not(tacheiAjoutee):
            listeDesLignes.append(
                'T' + str(i+1) + ';' + '0' + ';' + ';' + ';')
    return listeDesLignes


def creationFichier(nomFichier, nMethode, X, h, EmployeesDico):
    """nomFichier est le nom du fichier utilisée pour créer les variables globales.
    n_methode est le numéro de la méthode utilisée.
    X est un tableau en 3 dimensions où chaque coefficient permet de savoir si l'employé n est allé de la tâche i à la tâche j.
    Ne renvoie rien mais crée ou modifie le fichier .txt."""
    fichier = open(nomFichierResolution(nomFichier, nMethode), "w")
    fichier.write("\n".join(lignesSolution(X, h, EmployeesDico)))
    fichier.close()
    return None
