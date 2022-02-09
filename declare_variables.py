# Modules de base
import numpy as np
import matplotlib.pyplot as plt

# Module relatif à Gurobi
from gurobipy import *

m = Model("attribution_V1")

# importation des dictionnaires d'entrée

# a = np.array([[1,2],[3,4]])
# b = np.array([[[1,0],[0,3]],[[1,0],[0,3]]])
# print(np.tensordot(b,a))

# Ajout des variables de décision

X = m.addMVar(shape = (n_ouvrier,n_taches,n_taches),vtype = GRB.BINARY)
H = m.addMVar(shape = (n_ouvrier,n_taches),vtype = GRB.CONTINOUS)

# Ajout des contraintes

A = np.ones((n_ouvrier,n_taches))
b = 2*np.ones(n_taches)

C1 = m.addConstr(np.tensordot(X,A) == b)
C2 = m.addConstr()

print(X)

