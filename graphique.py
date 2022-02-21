import matplotlib.pyplot as plt


def affichage_graphique(lattitudes, longitudes, solutions):
    plt.plot(longitudes, lattitudes, "o")
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

affichage_graphique(lattitudes, longitudes, 1)
