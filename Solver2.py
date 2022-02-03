import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from scipy.optimize import fsolve
from cv2 import cv2 as cv


def traitement(dim_cible, coord_m1, coord_m2, coord_m3, data):
    """
    Parametres : 
        dim_cible : (largeur*hauteur) en mètres
        coord_mi : (xi,yi) coordonnées du micro i
        data : [(ordre micro i, délai absolu entre signal micro i et le premier)]
    Remarque :
        coordonnées avec un repère placé au centre de la cible"""

    tab_coord = [coord_m1, coord_m2, coord_m3]

    ordre_micro = [couple[0] for couple in data]
    deltaD12 = data[1][1]
    deltaD13 = data[2][1]

    tab_coord_ordre = []

    for i in ordre_micro:
        tab_coord_ordre.append(tab_coord[i-1])

    [(x1, y1), (x2, y2), (x3, y3)] = tab_coord_ordre

    largeur, hauteur = dim_cible

    mpl.rcParams['lines.color'] = 'k'
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler('color', ['k'])

    # 400 points par dimensions modifiable
    x = np.linspace(-largeur/2, largeur/2, 400)
    y = np.linspace(-hauteur/2, hauteur/2, 400)

    x, y = np.meshgrid(x, y)

    def axes():
        plt.axhline(0, alpha=.1)
        plt.axvline(0, alpha=.1)

    def parabole1(x, y):
        return 4*(deltaD12**2)*((x-x2)**2+(y-y2)**2) - ((x-x1)**2 + (y-y1)**2 - (x-x2)**2 - (y-y2)**2 - deltaD12**2)**2

    def parabole2(x, y):
        return 4*(deltaD13**2)*((x-x3)**2+(y-y3)**2) - ((x-x1)**2 + (y-y1)**2 - (x-x3)**2 - (y-y3)**2 - deltaD13**2)**2

    def f(input):
        xi, yi = input
        res = np.zeros(2)
        res[0] = parabole1(xi, yi)
        res[1] = parabole2(xi, yi)
        return res

    x0 = np.array(tab_coord_ordre[0])
    solution = fsolve(f, x0)
    print(solution)

    img_cible = cv.imread('.\public\cible.png')
    img_cible = cv.resize(img_cible, (700, 700), interpolation=cv.INTER_AREA)
    w, h = img_cible.shape[:2]
    cv.circle(img_cible, (int(
        solution[0]*w+(w/2)), int((h/2)-solution[1]*h)), 15, (0, 255, 0), thickness=2)

    font = cv.FONT_HERSHEY_SIMPLEX
    cv.putText(img_cible, "M1", (int(x1*w+(w/2))-15,
               int((h/2)-y1*h)+20), font, 0.7, (0, 255, 0))
    cv.putText(img_cible, "M2", (int(x2*w+(w/2)),
               int((h/2)-y2*h)-5), font, 0.7, (0, 255, 0))
    cv.putText(img_cible, "M3", (int(x3*w+(w/2))-35,
               int((h/2)-y3*h)-5), font, 0.7, (0, 255, 0))

    cv.imshow('cible', img_cible)
    cv.waitKey(0)

    axes()

    plt.contour(x, y, parabole1(x, y), [0], colors='k')
    plt.contour(x, y, parabole2(x, y), [0], colors='r')

    # plt.show()


delai12 = float(
    input("Entrer le délai (en mètres) entre le micro 1 et le micro 2 : "))
delai13 = float(
    input("Entrer le délai (en mètres) entre le micro 1 et le micro 3 : "))
traitement((1, 1), (0, 0.5), (-0.5, -0.5), (0.5, -0.5),
           [(1, 0), (2, delai12), (3, delai13)])  # delai entre 0 et 0.5
