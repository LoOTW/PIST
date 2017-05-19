"REMARQUES GENERALES : VARIABLES"
# la matrice coord == le corps du Snake
# la matrice spots == la plateau de jeu
from keras.optimizers import Adam

"Importation modules utiles"
from collections import deque, namedtuple
import sys
import os
import random
import pygame
import socket
import select
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from pathlib import Path



#INPUTS DE TEST
step=5000
END=500*step
EPS = [0.8, 0]
EPSSTEPS=(EPS[0]-EPS[1])/(END/2)
ALPHA=0.01
GAMMA=0.7
lenExpMax = 30000
samplesSize = 3200
batch = 32
epochs=10
#S'il n'y a qu'une seule couche le deuxième chiffre n'est pas pris en compte
NB_NEURONES=6
#IMPOOOOOOORTANT

#Si on entre trois paramètres avec le programme, remplace les valeurs au dessus
if len(sys.argv)==4:
    ALPHA=float(sys.argv[1])
    GAMMA=float(sys.argv[2])
    NB_NEURONES=int(sys.argv[3])

"Creation fichier enregistrement"
my_file = Path("model.json")
if my_file.is_file():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights("model.h5")

else:
    "creation nouveau neural network"
    model = Sequential()
    model.add(Dense(input_dim=10, output_dim=3))
    model.add(Dense(NB_NEURONES, activation='relu'))
    model.add(Dense(3))
optimizer=Adam(lr=ALPHA)
model.compile(loss='mse', optimizer=optimizer)

'DEF DES CARACTERISTIQ' \
'UES DU JEU'
# vitesse du Snake


#OUTPUTS DE TEST
PASAVANTMORT=[]
LOSSES=[]
DEFEATS=[]
VICTORIES=[]
RATIOS=[]
EPSILONS=[]
RATIOSSINGLE=[0]

#INTERMEDIAIRES DE CALCULS
ratioSingle=[0]
LOSS=[0]
FOUND=[0]
LOST=[0]
PAS=[0]



IHM=False
speed = 5000
BOARD_LENGTH = 32
OFFSET = 16
WHITE = (255, 255, 255)
BLACK = (12, 35 , 64)
RED = (164, 210, 51)
BLUE = (0, 184, 222)
EXP = []

COMPTEUR = [0]


DIRECTIONS = namedtuple('DIRECTIONS',
                        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)

"INITIALISATION MATRICE Q"
# Q = dict()
##lettre = ["v", "t", "p"] = [0, 1, 2]
# for i in range(-1*BOARD_LENGTH, BOARD_LENGTH+1):
#    for j in range(-1*BOARD_LENGTH, BOARD_LENGTH+1):
#        for m in range(3):
#            for n in range(3):
#                for o in range(3):
#                    Q[str(i)+"_"+str(j)+str(m)+str(n)+str(o)] = [5*random.random(), 5*random.random(), 5*random.random()]


"COLORATION ALEATOIRE SUPER SWAG DU SNAKE"


def rand_color():
    return (random.randrange(254) | 64, random.randrange(254) | 64, random.randrange(254) | 64)


def encoreUnMapping(board, snake, head):
    input = []

    (X, Y) = next(((i, row.index(2)) for i, row in enumerate(board) if 2 in row), (0, 0))
    XRelatif = head[0] - X  # X Relatif
    YRelatif = head[1] - Y  # Y Relatif

    currentDirection = snake.direction
    xTete = head[0]
    yTete = head[1]
    dead4sure = xTete < 0 or xTete >= BOARD_LENGTH or yTete < 0 or yTete >= BOARD_LENGTH

    distance = 1
    # Si dirige vers le haut
    if currentDirection == DIRECTIONS.Up:
        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            input.extend([distance, 0, 0, 0])
        elif (XRelatif < 0 and YRelatif == 0):
            input += [distance, distance, 0, 0]
        elif (XRelatif < 0 and YRelatif > 0):
            input.extend([0, distance, 0, 0])
        elif (XRelatif == 0 and YRelatif > 0):
            input += [0, distance, distance, 0]
        elif (XRelatif > 0 and YRelatif > 0):
            input.extend([0, 0, distance, 0])
        elif (XRelatif > 0 and YRelatif == 0):
            input += [0, 0, distance, distance]
        elif (XRelatif > 0 and YRelatif < 0):
            input.extend([0, 0, 0, distance])
        elif (XRelatif == 0 and YRelatif < 0):
            input.extend([distance, 0, 0, distance])
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([distance, distance, distance, distance])

        # Création des 3 inputs

        # A gauche
        if dead4sure or yTete == 0 or board[xTete][yTete - 1] == 1:
            input.append(1)
        else:
            input.append(0)

        # En haut
        if dead4sure or xTete == 0 or board[xTete - 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

        # A droite
        if dead4sure or yTete == BOARD_LENGTH - 1 or board[xTete][yTete + 1] == 1:
            input.append(1)
        else:
            input.append(0)

    # Si dirige vers la droite
    if currentDirection == DIRECTIONS.Right:
        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            input.extend([0, 0, 0, distance])
        elif (XRelatif < 0 and YRelatif == 0):
            input.extend([distance, 0, 0, distance])
        elif (XRelatif < 0 and YRelatif > 0):
            input.extend([distance, 0, 0, 0])
        elif (XRelatif == 0 and YRelatif > 0):
            input += [distance, distance, 0, 0]
        elif (XRelatif > 0 and YRelatif > 0):
            input.extend([0, distance, 0, 0])
        elif (XRelatif > 0 and YRelatif == 0):
            input += [0, distance, distance, 0]
        elif (XRelatif > 0 and YRelatif < 0):
            input.extend([0, 0, distance, 0])
        elif (XRelatif == 0 and YRelatif < 0):
            input += [0, 0, distance, distance]
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([distance, distance, distance, distance])

        # Création des 3 inputs

        # En haut
        if dead4sure or xTete == 0 or board[xTete - 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

        # A droite
        if dead4sure or yTete == BOARD_LENGTH - 1 or board[xTete][yTete + 1] == 1:
            input.append(1)
        else:
            input.append(0)

        # En bas
        if dead4sure or xTete == BOARD_LENGTH - 1 or board[xTete + 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

    # Si dirige vers le bas
    if currentDirection == DIRECTIONS.Down:

        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            input.extend([0, 0, distance, 0])
        elif (XRelatif < 0 and YRelatif == 0):
            input += [0, 0, distance, distance]
        elif (XRelatif < 0 and YRelatif > 0):
            input.extend([0, 0, 0, distance])
        elif (XRelatif == 0 and YRelatif > 0):
            input.extend([distance, 0, 0, distance])
        elif (XRelatif > 0 and YRelatif > 0):
            input.extend([distance, 0, 0, 0])
        elif (XRelatif > 0 and YRelatif == 0):
            input += [distance, distance, 0, 0]
        elif (XRelatif > 0 and YRelatif < 0):
            input.extend([0, distance, 0, 0])
        elif (XRelatif == 0 and YRelatif < 0):
            input += [0, distance, distance, 0]
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([distance, distance, distance, distance])

        # Création des 3 inputs

        # A droite
        if dead4sure or yTete == BOARD_LENGTH - 1 or board[xTete][yTete + 1] == 1:
            input.append(1)
        else:
            input.append(0)

        # En bas
        if dead4sure or xTete == BOARD_LENGTH - 1 or board[xTete + 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

        # A gauche
        if dead4sure or yTete == 0 or board[xTete][yTete - 1] == 1:
            input.append(1)
        else:
            input.append(0)

    # Si dirige vers la gauche
    if currentDirection == DIRECTIONS.Left:

        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            input.extend([0, distance, 0, 0])
        elif (XRelatif < 0 and YRelatif == 0):
            input += [0, distance, distance, 0]
        elif (XRelatif < 0 and YRelatif > 0):
            input.extend([0, 0, distance, 0])
        elif (XRelatif == 0 and YRelatif > 0):
            input += [0, 0, distance, distance]
        elif (XRelatif > 0 and YRelatif > 0):
            input.extend([0, 0, 0, distance])
        elif (XRelatif > 0 and YRelatif == 0):
            input.extend([distance, 0, 0, distance])
        elif (XRelatif > 0 and YRelatif < 0):
            input.extend([distance, 0, 0, 0])
        elif (XRelatif == 0 and YRelatif < 0):
            input += [distance, distance, 0, 0]
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([distance, distance, distance, distance])

            # Création des 3 inputs

            # En bas
        if dead4sure or xTete == BOARD_LENGTH - 1 or board[xTete + 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

        # A gauche
        if dead4sure or yTete == 0 or board[xTete][yTete - 1] == 1:
            input.append(1)
        else:
            input.append(0)

        # En haut
        if dead4sure or xTete == 0 or board[xTete - 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)
    return input


def mappingHybride(board, snake, head):
    input = []

    xTete = head[0]
    yTete = head[1]
    dead4sure = xTete < 0 or xTete >= BOARD_LENGTH or yTete < 0 or yTete >= BOARD_LENGTH


    # Cherche les coordonnees de la pomme
    X = 0
    Y = 0
    for i in range(BOARD_LENGTH):
        stop = False
        for j in range(BOARD_LENGTH):
            if board[i][j] == 2:
                X = i
                Y = j
                stop = True
                break
        if stop:
            break

    XRelatif = head[0] - X  # X Relatif
    YRelatif = head[1] - Y  # Y Relatif

    currentDirection = snake.direction
    xTete = head[0]
    yTete = head[1]
    x = xTete
    y = yTete
    distance = 1
    trouve = False
    # Si dirige vers le haut
    if currentDirection == DIRECTIONS.Up:
        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            input += [distance, 0, 0, 0]
        elif (XRelatif < 0 and YRelatif == 0):
            input += [distance, distance, 0, 0]
        elif (XRelatif < 0 and YRelatif > 0):
            input += [0, distance, 0, 0]
        elif (XRelatif == 0 and YRelatif > 0):
            input += [0, distance, distance, 0]
        elif (XRelatif > 0 and YRelatif > 0):
            input += [0, 0, distance, 0]
        elif (XRelatif > 0 and YRelatif == 0):
            input += [0, 0, distance, distance]
        elif (XRelatif > 0 and YRelatif < 0):
            input += [0, 0, 0, distance]
        elif (XRelatif == 0 and YRelatif < 0):
            input += [distance, 0, 0, distance]
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([distance, distance, distance, distance])

        # Création des 3 inputs
        if dead4sure:
            input.extend([1, 1, 1])
        else :
            # A gauche
            while y >= 0 and not trouve:
                y -= 1
                if board[xTete][y] == 1:
                    trouve = True
                    dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                input += [dist]
            y = yTete
            trouve = False

            # En haut
            while x >= 0 and not trouve:
                x -= 1
                if board[x][yTete] == 1:
                    trouve = True
                    dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                input += [dist]
            x = xTete
            trouve = False

            # A droite
            while y < BOARD_LENGTH - 1 and not trouve:
                y += 1
                if board[xTete][y] == 1:
                    trouve = True
                    dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                input += [dist]
            y = yTete
            trouve = False

        # Input Mur
        # A gauche
        if dead4sure or yTete == 0 or board[xTete][yTete - 1] == 1:
            input.append(1)
        else:
            input.append(0)

        # En haut
        if dead4sure or xTete == 0 or board[xTete - 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

        # A droite
        if dead4sure or yTete == BOARD_LENGTH - 1 or board[xTete][yTete + 1] == 1:
            input.append(1)
        else:
            input.append(0)

    # Si dirige vers la droite
    if currentDirection == DIRECTIONS.Right:
        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            input += [0, 0, 0, distance]
        elif (XRelatif < 0 and YRelatif == 0):
            input += [distance, 0, 0, distance]
        elif (XRelatif < 0 and YRelatif > 0):
            input += [distance, 0, 0, 0]
        elif (XRelatif == 0 and YRelatif > 0):
            input += [distance, distance, 0, 0]
        elif (XRelatif > 0 and YRelatif > 0):
            input += [0, distance, 0, 0]
        elif (XRelatif > 0 and YRelatif == 0):
            input += [0, distance, distance, 0]
        elif (XRelatif > 0 and YRelatif < 0):
            input += [0, 0, distance, 0]
        elif (XRelatif == 0 and YRelatif < 0):
            input += [0, 0, distance, distance]
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([distance, distance, distance, distance])

        # Création des 3 inputs
        if dead4sure:
            input.extend([1, 1, 1])
        else:
            # En haut
            while x >= 0 and not trouve:
                x -= 1
                if board[x][yTete] == 1:
                    trouve = True
                    dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                input += [dist]
            x = xTete
            trouve = False

            # A droite
            while y < BOARD_LENGTH - 1 and not trouve:
                y += 1
                if board[xTete][y] == 1:
                    trouve = True
                    dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                input += [dist]
            y = yTete
            trouve = False

            # En bas
            while x < BOARD_LENGTH - 1 and not trouve:
                x += 1
                if board[x][yTete] == 1:
                    trouve = True
                    dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                input += [dist]
            x = xTete
            trouve = False

        # InputMur
        # En haut
        if dead4sure or xTete == 0 or board[xTete - 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

        # A droite
        if dead4sure or yTete == BOARD_LENGTH - 1 or board[xTete][yTete + 1] == 1:
            input.append(1)
        else:
            input.append(0)

        # En bas
        if dead4sure or xTete == BOARD_LENGTH - 1 or board[xTete + 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

    # Si dirige vers le bas
    if currentDirection == DIRECTIONS.Down:

        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            input += [0, 0, distance, 0]
        elif (XRelatif < 0 and YRelatif == 0):
            input += [0, 0, distance, distance]
        elif (XRelatif < 0 and YRelatif > 0):
            input += [0, 0, 0, distance]
        elif (XRelatif == 0 and YRelatif > 0):
            input += [distance, 0, 0, distance]
        elif (XRelatif > 0 and YRelatif > 0):
            input += [distance, 0, 0, 0]
        elif (XRelatif > 0 and YRelatif == 0):
            input += [distance, distance, 0, 0]
        elif (XRelatif > 0 and YRelatif < 0):
            input += [0, distance, 0, 0]
        elif (XRelatif == 0 and YRelatif < 0):
            input += [0, distance, distance, 0]
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([distance, distance, distance, distance])

        # Création des 3 inputs
        if dead4sure:
            input.extend([1, 1, 1])
        else:
            # A droite
            while y < BOARD_LENGTH - 1 and not trouve:
                y += 1
                if board[xTete][y] == 1:
                    trouve = True
                    dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                input += [dist]
            y = yTete
            trouve = False

            # En bas
            while x < BOARD_LENGTH - 1 and not trouve:
                x += 1
                if board[x][yTete] == 1:
                    trouve = True
                    dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                input += [dist]
            x = xTete
            trouve = False

            # A gauche
            while y >= 0 and not trouve:
                y -= 1
                if board[xTete][y] == 1:
                    trouve = True
                    dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                input += [dist]
            y = yTete
            trouve = False

        # InputMur
        # A droite
        if dead4sure or yTete == BOARD_LENGTH - 1 or board[xTete][yTete + 1] == 1:
            input.append(1)
        else:
            input.append(0)

        # En bas
        if dead4sure or xTete == BOARD_LENGTH - 1 or board[xTete + 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

        # A gauche
        if dead4sure or yTete == 0 or board[xTete][yTete - 1] == 1:
            input.append(1)
        else:
            input.append(0)

    # Si dirige vers la gauche
    if currentDirection == DIRECTIONS.Left:

        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            input += [0, distance, 0, 0]
        elif (XRelatif < 0 and YRelatif == 0):
            input += [0, distance, distance, 0]
        elif (XRelatif < 0 and YRelatif > 0):
            input += [0, 0, distance, 0]
        elif (XRelatif == 0 and YRelatif > 0):
            input += [0, 0, distance, distance]
        elif (XRelatif > 0 and YRelatif > 0):
            input += [0, 0, 0, distance]
        elif (XRelatif > 0 and YRelatif == 0):
            input += [distance, 0, 0, distance]
        elif (XRelatif > 0 and YRelatif < 0):
            input += [distance, 0, 0, 0]
        elif (XRelatif == 0 and YRelatif < 0):
            input += [distance, distance, 0, 0]
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([distance, distance, distance, distance])

            # Création des 3 inputs

        if dead4sure:
           input.extend([1, 1, 1])
        else:
            # En bas
            while x < BOARD_LENGTH - 1 and not trouve:
                x += 1
                if board[x][yTete] == 1:
                    trouve = True
                    dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                input += [dist]
            x = xTete
            trouve = False

            # A gauche
            while y >= 0 and not trouve:
                y -= 1
                if board[xTete][y] == 1:
                    trouve = True
                    dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(y - yTete)) / BOARD_LENGTH)
                input += [dist]
            y = yTete
            trouve = False

            # En haut
            while x >= 0 and not trouve:
                x -= 1
                if board[x][yTete] == 1:
                    trouve = True
                    dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                    input += [dist]
            if not trouve:
                dist = (1 - (abs(x - xTete)) / BOARD_LENGTH)
                input += [dist]
            x = xTete
            trouve = False

        # InputMur
        # En bas
        if dead4sure or xTete == BOARD_LENGTH - 1 or board[xTete + 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)

        # A gauche
        if dead4sure or yTete == 0 or board[xTete][yTete - 1] == 1:
            input.append(1)
        else:
            input.append(0)

        # En haut
        if dead4sure or xTete == 0 or board[xTete - 1][yTete] == 1:
            input.append(1)
        else:
            input.append(0)


    return input

# Crée 7 inputs :
# 4 inputs correspondants à la présence de la pomme dans les 4 carrés autour du snake
# 3 inputs correspondants à la distance tête snake <-> obstacle à G, devant et à D
def mappingCarre(board, snake, head):
    input = []

    # Cherche les coordonnees de la pomme
    (X, Y) = next(((i, row.index(2)) for i, row in enumerate(board) if 2 in row), (0, 0))
    XRelatif = head[0] - X  # X Relatif
    YRelatif = head[1] - Y  # Y Relatif

    currentDirection = snake.direction
    xTete = head[0]
    yTete = head[1]
    x = xTete
    y = yTete

    trouve = False

    # Si dirige vers le haut
    if currentDirection == DIRECTIONS.Up:
        # Création des 4 inputs

        if (XRelatif < 0 and YRelatif < 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([distance, 0, 0, 0])
        elif (XRelatif < 0 and YRelatif == 0):
            distance = 1 - (abs(XRelatif)) / BOARD_LENGTH
            input.extend([distance, distance, 0, 0])
        elif (XRelatif < 0 and YRelatif > 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, distance, 0, 0])
        elif (XRelatif == 0 and YRelatif > 0):
            distance = 1 - (abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, distance, distance, 0])
        elif (XRelatif > 0 and YRelatif > 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, distance, 0])
        elif (XRelatif > 0 and YRelatif == 0):
            distance = 1 - (abs(XRelatif)) / BOARD_LENGTH
            input.extend([0, 0, distance, distance])
        elif (XRelatif > 0 and YRelatif < 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, 0, distance])
        elif (XRelatif == 0 and YRelatif < 0):
            distance = 1 - (abs(YRelatif)) / BOARD_LENGTH
            input.extend([distance, 0, 0, distance])
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([1, 1, 1, 1])

        # Création des 3 inputs
        if xTete < 0 or xTete >= BOARD_LENGTH or yTete < 0 or yTete >= BOARD_LENGTH:
            input.extend([1, 1, 1])
        else :
            # A gauche
            while y >= 0 and not trouve:
                y -= 1
                if board[xTete][y] == 1:
                    trouve = True
                    distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                input.append(distance)
            y = yTete
            trouve = False

            # En haut
            while x >= 0 and not trouve:
                x -= 1
                if board[x][yTete] == 1:
                    trouve = True
                    distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                input.append(distance)
            x = xTete
            trouve = False

            # A droite
            while y < BOARD_LENGTH - 1 and not trouve:
                y += 1
                if board[xTete][y] == 1:
                    trouve = True
                    distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                input.append(distance)
            y = yTete
            trouve = False

    # Si dirige vers la droite
    if currentDirection == DIRECTIONS.Right:
        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, 0, distance])
        elif (XRelatif < 0 and YRelatif == 0):
            distance = 1 - (abs(XRelatif)) / BOARD_LENGTH
            input.extend([distance, 0, 0, distance])
        elif (XRelatif < 0 and YRelatif > 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([distance, 0, 0, 0])
        elif (XRelatif == 0 and YRelatif > 0):
            distance = 1 - (abs(YRelatif)) / BOARD_LENGTH
            input.extend([distance, distance, 0, 0])
        elif (XRelatif > 0 and YRelatif > 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, distance, 0, 0])
        elif (XRelatif > 0 and YRelatif == 0):
            distance = 1 - (abs(XRelatif)) / BOARD_LENGTH
            input.extend([0, distance, distance, 0])
        elif (XRelatif > 0 and YRelatif < 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, distance, 0])
        elif (XRelatif == 0 and YRelatif < 0):
            distance = 1 - (abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, distance, distance])
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([1, 1, 1, 1])

        # Création des 3 inputs
        if xTete < 0 or xTete >= BOARD_LENGTH or yTete < 0 or yTete >= BOARD_LENGTH:
            input.extend([1, 1, 1])
        else :
            # En haut
            while x >= 0 and not trouve:
                x -= 1
                if board[x][yTete] == 1:
                    trouve = True
                    distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                input.append(distance)
            x = xTete
            trouve = False

            # A droite
            while y < BOARD_LENGTH - 1 and not trouve:
                y += 1
                if board[xTete][y] == 1:
                    trouve = True
                    distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                input.append(distance)
            y = yTete
            trouve = False

            # En bas
            while x < BOARD_LENGTH - 1 and not trouve:
                x += 1
                if board[x][yTete] == 1:
                    trouve = True
                    distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                input.append(distance)
            x = xTete
            trouve = False

    # Si dirige vers le bas
    if currentDirection == DIRECTIONS.Down:
        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, distance, 0])
        elif (XRelatif < 0 and YRelatif == 0):
            distance = 1 - (abs(XRelatif)) / BOARD_LENGTH
            input.extend([0, 0, distance, distance])
        elif (XRelatif < 0 and YRelatif > 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, 0, distance])
        elif (XRelatif == 0 and YRelatif > 0):
            distance = 1 - (abs(YRelatif)) / BOARD_LENGTH
            input.extend([distance, 0, 0, distance])
        elif (XRelatif > 0 and YRelatif > 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([distance, 0, 0, 0])
        elif (XRelatif > 0 and YRelatif == 0):
            distance = 1 - (abs(XRelatif)) / BOARD_LENGTH
            input.extend([distance, distance, 0, 0])
        elif (XRelatif > 0 and YRelatif < 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, distance, 0, 0])
        elif (XRelatif == 0 and YRelatif < 0):
            distance = 1 - (abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, distance, distance, 0])
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([1, 1, 1, 1])

        # Création des 3 inputs

        # A droite
        if xTete < 0 or xTete >= BOARD_LENGTH or yTete < 0 or yTete >= BOARD_LENGTH:
            input.extend([1, 1, 1])
        else :
            while y < BOARD_LENGTH - 1 and not trouve:
                y += 1
                if board[xTete][y] == 1:
                    trouve = True
                    distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                input.append(distance)
            y = yTete
            trouve = False

            # En bas
            while x < BOARD_LENGTH - 1 and not trouve:
                x += 1
                if board[x][yTete] == 1:
                    trouve = True
                    distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                input.append(distance)
            x = xTete
            trouve = False

            # A gauche
            while y >= 0 and not trouve:
                y -= 1
                if board[xTete][y] == 1:
                    trouve = True
                    distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                input.append(distance)
            y = yTete
            trouve = False

    # Si dirige vers la gauche
    if currentDirection == DIRECTIONS.Left:

        # Création des 4 inputs
        if (XRelatif < 0 and YRelatif < 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, distance, 0, 0])
        elif (XRelatif < 0 and YRelatif == 0):
            distance = 1 - (abs(XRelatif)) / BOARD_LENGTH
            input.extend([0, distance, distance, 0])
        elif (XRelatif < 0 and YRelatif > 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, distance, 0])
        elif (XRelatif == 0 and YRelatif > 0):
            distance = 1 - (abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, distance, distance])
        elif (XRelatif > 0 and YRelatif > 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([0, 0, 0, distance])
        elif (XRelatif > 0 and YRelatif == 0):
            distance = 1 - (abs(XRelatif)) / BOARD_LENGTH
            input.extend([distance, 0, 0, distance])
        elif (XRelatif > 0 and YRelatif < 0):
            distance = 1 - (abs(XRelatif) + abs(YRelatif)) / BOARD_LENGTH
            input.extend([distance, 0, 0, 0])
        elif (XRelatif == 0 and YRelatif < 0):
            distance = 1 - (abs(YRelatif)) / BOARD_LENGTH
            input.extend([distance, distance, 0, 0])
        elif (XRelatif == 0 and YRelatif == 0):
            input.extend([1, 1, 1, 1])

            # Création des 3 inputs
        if xTete < 0 or xTete >= BOARD_LENGTH or yTete < 0 or yTete >= BOARD_LENGTH:
            input.extend([1, 1, 1])
        else:
            #  En bas
            while x < BOARD_LENGTH - 1 and not trouve:
                x += 1
                if board[x][yTete] == 1:
                    trouve = True
                    distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(x - xTete) / BOARD_LENGTH)
                input.append(distance)
            x = xTete
            trouve = False

            # A gauche
            while y >= 0 and not trouve:
                y -= 1
                if board[xTete][y] == 1:
                    trouve = True
                    distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                input.append(distance)
            y = yTete
            trouve = False

            # A droite
            while y < BOARD_LENGTH - 1 and not trouve:
                y += 1
                if board[xTete][y] == 1:
                    trouve = True
                    distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                    input.append(distance)
            if not trouve:
                distance = 1 - (abs(y - yTete) / BOARD_LENGTH)
                input.append(distance)
    return input


"ASSOCIE A TOUT ETAT POSSIBLE UN CODE UNIQUE (A PARTIR DES LA POSITION + ETAT VOISINS"

# "['case qui tue','case vide','case pomme']  = [0,1,2]
def code_etat(position, voisins, food, spots):
    s = ""
    #print("Je suis en " + str(position))
    #print("Mes voisins sont : " + str(voisins))
    # ecart selon les x
    s += str(position[0] - food[0]) + "_"

    # ecart selon les y
    s += str(position[1] - food[1])

    # obtention etats cases voisines
    for i in range(3):
        v = voisins[i]
        if (v[0] < 0 or v[0] >= BOARD_LENGTH or v[1] < 0 or v[1] >= BOARD_LENGTH):
            s += "0"
        else:
            if spots[v[0]][v[1]] == 0:
                s += "1"
            elif spots[v[0]][v[1]] == 1:
                s += "0"
            else:
                s += "2"
   #print("Mon état est donc " +str(s))
    return s
# "['case qui tue','case vide','case pomme']  = [0,1,2]
def nextPosition(voisins, spots, directionRelative):
    s=0
    # obtention etats cases voisines

    v = voisins[directionRelative]
    if (v[0] < 0 or v[0] >= BOARD_LENGTH or v[1] < 0 or v[1] >= BOARD_LENGTH):
        s = 0
    else:
        if spots[v[0]][v[1]] == 0:
            s = 1
        elif spots[v[0]][v[1]] == 1:
            s = 0
        else:
            s = 2
    return s
"'CREATION CLASSE SNAKE"


# demarre initialement au milieu du board ie aux coordonnees (16,16), en se dirigeant vers la droite
# remarque : deque == type d'objet (en gros une liste chainee)

class Snake(object):
    def __init__(self, direction=DIRECTIONS.Right, point=(16, 16, BLUE), color=None):
        # taille max sachant nb popommes mangees
        self.tailmax = 4

        # dir acuelle
        self.direction = direction

        # coord points du serpent (le dernier elem == tete)
        # ie head == self.deque[self.deque.__len__-1][self.deque.__len__-1]
        self.deque = deque()
        self.deque.append(point)

        # couleur (obviously)
        self.color = BLUE

        # prochaine direction (je sais pas pourquoi il faut un deque et pas juste unelement ici en vrai)
        self.nextDir = deque()

        # etat Snake
        self.state = ""

        # mat recompense
        #self.rewardMatrix = [[] for i in range(BOARD_LENGTH + 2)]

        # exp replay
        self.experience = EXP

        # politique decision
        self.Q = np.array([[0, 0, 0]])

    def get_color(self):
        return BLUE

    "RETOURNE LA LISTE [voisin gauche, voisin devant, voisin droite]"

    def voisins(self, head):
        i = head[0]
        j = head[1]
        V = []

        if (self.direction == DIRECTIONS.Up):
            V.append([i, j - 1])
            V.append([i - 1, j])
            V.append([i, j + 1])

        elif (self.direction == DIRECTIONS.Right):
            V.append([i - 1, j])
            V.append([i, j + 1])
            V.append([i + 1, j])

        elif (self.direction == DIRECTIONS.Down):
            V.append([i, j + 1])
            V.append([i + 1, j])
            V.append([i, j - 1])

        elif (self.direction == DIRECTIONS.Left):
            V.append([i + 1, j])
            V.append([i, j - 1])
            V.append([i - 1, j])
        return V

    "donne actions possibles (directions relatives pour Snake) a partir de directions absolues (par rapport au plateau)"

    def trad_direction(self, nv_dir):
        if (self.direction == DIRECTIONS.Up):
            if nv_dir == 0:
                return DIRECTIONS.Left
            if nv_dir == 1:
                return DIRECTIONS.Up
            else:
                return DIRECTIONS.Right

        elif (self.direction == DIRECTIONS.Right):
            if nv_dir == 0:
                return DIRECTIONS.Up
            if nv_dir == 1:
                return DIRECTIONS.Right
            else:
                return DIRECTIONS.Down

        elif (self.direction == DIRECTIONS.Down):
            if nv_dir == 0:
                return DIRECTIONS.Right
            if nv_dir == 1:
                return DIRECTIONS.Down
            else:
                return DIRECTIONS.Left

        elif (self.direction == DIRECTIONS.Left):
            if nv_dir == 0:
                return DIRECTIONS.Down
            if nv_dir == 1:
                return DIRECTIONS.Left
            else:
                return DIRECTIONS.Up

    # choix prochaine direction
    def populate_nextDir(self, events, identifier):
        "Code pour direction automatique du serpent"
        aleat = random.randrange(0, 3)
        tirage = random.random()

        "Cas ou le serpent explore --> direction aleat"
        if EPS[0] > EPS[1]:
            EPS[0] -= EPSSTEPS

        if tirage < EPS[0]:
            self.nextDir.appendleft(self.trad_direction(aleat))

            return aleat

        # Cas ou le serpent exploite la politique de decision d action du QLearning
        else:

            if self.Q.argmax() == 0:
                self.nextDir.appendleft(self.trad_direction(0))
                return 0
            elif self.Q.argmax() == 1:
                self.nextDir.appendleft(self.trad_direction(1))
                return 1
            else:
                self.nextDir.appendleft(self.trad_direction(2))
                return 2


'FONCTION PLACANT LA POPOMME'

def find_food(spots):
    while True:
        food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[food[0]][food[1]] == 1 or
                         spots[food[0]][food[1]] == 2)):
            break
    return food


'FONCTION TESTANT LES DEUX CONDITIONS DE GAMEOVER'

def end_condition(board, coord):
    # teste si le Snake vient de se manger salement le mur
    if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or
                coord[1] >= BOARD_LENGTH):
        return True
    # teste si le Snake vient de se manger stupidement la queue
    if (board[coord[0]][coord[1]] == 1):
        return True
    return False

"FONCTION CREANT L AIRE DE JEU"

# l aire de jeu est representee par la liste de liste spots
def make_board():

    return [[0 for i in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]

"FONCTION RETOURNANT LA RECOMPENSE POUR UNE ACTION"

def get_reward(old_state, directionRelative):
    tete = int(old_state[len(old_state)-1-(2-directionRelative)])
    if(tete<32 and tete>=0 and tete<32 and tete>=0):
        #print(tete[0])
        #print(tete[1])
        if tete == 0:
            return -20
        elif tete== 1:
            return -1
        elif tete ==2:
            return 50
    else:
        return -20

def getRewardMappingCarre(directionRelative, voisins, spots):
    nextPositionValue=nextPosition(voisins, spots, directionRelative)
    #print("La valeur de la case suivante est :" +str(nextPositionValue))
    if (nextPositionValue==0):
        return -20
    elif nextPositionValue == 1:
        return -1
    else:
        return 50

"MAJ DU TABLEAU DE JEU"

def update_board(screen, snakes, food):
    if IHM:
        rect = pygame.Rect(0, 0, OFFSET, OFFSET)

        # redef du tableau de jeu case par case
        spots = [[] for i in range(BOARD_LENGTH)]
        num1 = 0
        num2 = 0
        for row in spots:
            for i in range(BOARD_LENGTH):
                row.append(0)
                temprect = rect.move(num1 * OFFSET, num2 * OFFSET)
                pygame.draw.rect(screen, BLACK, temprect)
                num2 += 1
            num1 += 1

        # ca place la popomme
        spots[food[0]][food[1]] = 2

        temprect = rect.move(food[1] * OFFSET, food[0] * OFFSET)
        pygame.draw.rect(screen, RED, temprect)

        # ca renseigne ou qu il est le snake
        for snake in snakes:
            for coord in snake.deque:
                spots[coord[0]][coord[1]] = 1
                temprect = rect.move(coord[1] * OFFSET, coord[0] * OFFSET)
                pygame.draw.rect(screen, coord[2], temprect)
    else:
        spots = make_board()

        # ca place la popomme
        spots[food[0]][food[1]] = 2

        # ca renseigne ou qu il est le snake
        for snake in snakes:
            for coord in snake.deque:
                spots[coord[0]][coord[1]] = 1
    return spots


def get_color(s):
    if s == "bk":
        return BLACK
    elif s == "wh":
        return WHITE
    elif s == "rd":
        return RED
    elif s == "bl":
        return BLUE
    elif s == "fo":
        return rand_color()
    else:
        print("WHAT", s)
        return BLUE


"I DON T KNOW REALLY LOL"


def update_board_delta(screen, deltas):
    # accepts a queue of deltas in the form
    # [("d", 13, 30), ("a", 4, 6, "rd")]
    # valid colors: re, wh, bk, bl
    rect = pygame.Rect(0, 0, OFFSET, OFFSET)
    change_list = []
    delqueue = deque()
    addqueue = deque()
    while len(deltas) != 0:
        d = deltas.pop()
        change_list.append(pygame.Rect(d[1], d[2], OFFSET, OFFSET))
        if d[0] == "d":
            delqueue.append((d[1], d[2]))
        elif d[0] == "a":
            addqueue.append((d[1], d[2], get_color(d[3])))

    for d_coord in delqueue:
        temprect = rect.move(d_coord[1] * OFFSET, d_coord[0] * OFFSET)
        # TODO generalize background color
        pygame.draw.rect(screen, BLACK, temprect)

    for a_coord in addqueue:
        temprect = rect.move(a_coord[1] * OFFSET, a_coord[0] * OFFSET)
        pygame.draw.rect(screen, a_coord[2], temprect)

    return change_list


"DEF DU MENU DU SNAKE"


# Return 0 to exit the program, 1 for a one-player game
def menu(screen):
    font = pygame.font.Font(None, 30)
    menu_message1 = font.render("Press enter for one-player, t for two-player", True, WHITE)
    menu_message2 = font.render("C'est le PIST de l'ambiance", True, WHITE)

    screen.fill(BLACK)
    screen.blit(menu_message1, (32, 32))
    screen.blit(menu_message2, (32, 64))
    pygame.display.update()
    while True:
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 1
                if event.key == pygame.K_t:
                    return 2
                if event.key == pygame.K_l:
                    return 3
                if event.key == pygame.K_n:
                    return 4
        if done:
            break
    if done:
        pygame.quit()
        return 0


def quit(screen):
    return False


"FAIT SE DEPLACER LE SNAKE SELON LE DEPLACEMENT INDIQUE DANS LA DEQUE NEXTDIR + SA DIRCTION ACTUELLE"


def move(snake):
    if len(snake.nextDir) != 0:
        next_dir = snake.nextDir.pop()
    else:
        next_dir = snake.direction
    # direct = snake.direction
    head = snake.deque.pop()
    snake.deque.append(head)
    next_move = head

    if (next_dir == DIRECTIONS.Up):
        if snake.direction != DIRECTIONS.Down:
            next_move = (head[0] - 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move = (head[0] + 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Down):
        if snake.direction != DIRECTIONS.Up:
            next_move = (head[0] + 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move = (head[0] - 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Left):
        if snake.direction != DIRECTIONS.Right:
            next_move = (head[0], head[1] - 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move = (head[0], head[1] + 1, snake.get_color())
    elif (next_dir == DIRECTIONS.Right):
        if snake.direction != DIRECTIONS.Left:
            next_move = (head[0], head[1] + 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move = (head[0], head[1] - 1, snake.get_color())
    return next_move


"INDIQUE SI CASE == POPOMME"


def is_food(board, point):
    return board[point[0]][point[1]] == 2


"EXP REPLAY"


def end_cond(etat, action):
    if etat[len(etat) - 3] == '0' and action == 0:
        return True
    if etat[len(etat) - 2] == '0' and action == 1:
        return True
    if etat[len(etat) - 1] == '0' and action == 2:
        return True
    return False

def enregistrementModel(m):
    saveOnDisk("ratioSingle", RATIOSSINGLE)
    model_json = m.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    m.save_weights("model.h5")

def enregistrement():


    PASAVANTMORT.append(PAS[0]/(LOST[0]+1))
    LOSSES.append(LOSS[0])
    VICTORIES.append(FOUND[0])
    DEFEATS.append(LOST[0])
    RATIOS.append(FOUND[0] / (LOST[0] + 1))
    EPSILONS.append(EPS[0])



    print("Victoire : " + str(FOUND[0]) + " Défaites : " + str(LOST[0]) + " Ratio : " + str(FOUND[0] / (LOST[0] + 1))
          + " EPS : " + str(EPS[0]) + " LOSS : " + str(LOSS[0])+" ITERATIONS : "+str(COMPTEUR[0]/step))

    saveOnDisk("loss", LOSSES)
    saveOnDisk("epsilon",EPSILONS)
    saveOnDisk("victoires",VICTORIES)
    saveOnDisk("defaites", DEFEATS)
    saveOnDisk("ratios",RATIOS)
    saveOnDisk("pasAvantMort", PASAVANTMORT)
    LOST[0] = 0
    FOUND[0] = 0
    PAS[0]=0

def saveOnDisk(nomDuFichier, liste):
    with open(nomDuFichier+".txt", "w") as file:
        file.write(str(liste))


"VERSION UN JOUEUR"


# Return false to quit program, true to go to
# gameover screen
def one_player(screen):
    clock = pygame.time.Clock()
    spots = make_board()

    food = find_food(spots)
    spots[food[0]][food[1]]=2
    snake = Snake()
    ratioSingle=[0]
    currentHead = snake.deque[snake.deque.__len__() - 1]
    snake.state = mappingHybride(spots, snake, currentHead)
    #snake.rewardMatrix = snake.initializeRewardMatrix(food)

    while True:
        clock.tick(speed)
        # Event processing
        done = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
                break
        if done:
            return False


        "Game logic"

        old_state = snake.state
        temp = model.predict(np.array([old_state]))

        snake.Q=np.array([temp[0][0],temp[0][1],temp[0][2]])
        directionRelative=snake.populate_nextDir(events, "arrows")
        #print("Je suis en "+ str(snake.deque[-1]))
        voisins = snake.voisins(snake.deque[-1])

        #print("Les voisins sont : " + str(voisins))

        #print("je choisis " + str(directionRelative))

        next_head = move(snake)
        #print("Je serais en "+str(next_head))

        snake.state = mappingHybride(spots, snake, next_head)
        #new_state = snake.state

        "EXP REPLAY"

        recomp = getRewardMappingCarre(directionRelative, voisins, spots)
        #print("La récompense est "+str(recomp))
        snake.experience.append(
            [old_state, directionRelative, recomp, snake.state])


        if (len(snake.experience) > lenExpMax):
            snake.experience.pop(random.randrange(lenExpMax))

        PAS[0]+=1
        if(COMPTEUR[0]%step==0 and COMPTEUR[0]!=0):
            x_train=[]
            y_train=[]
            lenExp = len(snake.experience)
            if (lenExp >= batch):

                for i in range(samplesSize):
                    sample = random.choice(EXP)

                    oldState4Keras = sample[0]
                    Qmodif = model.predict(np.array([oldState4Keras]))
                    #print("Avant Q vaut : "+str(Qmodif))
                    if end_cond(sample[0], sample[1]):
                        Qmodif[0][sample[1]] = np.array([[sample[2]]])
                    else:
                        temp2 = model.predict(np.array([sample[3]]))
                        Qmodif[0][sample[1]] = np.array(sample[2] + GAMMA * temp2.max())
                    x_train.append(oldState4Keras)
                    y_train.append([Qmodif[0][0], Qmodif[0][1], Qmodif[0][2]])
                    #print("on ajoute "+str(sample[2] + GAMMA * temp2.max()))
                    #print("L'état est " + str(sample[0])+" La direction choisie est " + str(sample[1]))
                    #print("L'état suivant est " + str(sample[3]))
                    #print("La récompense est " + str(sample[2]))
                    #print("Après Q vaut : " + str(Qmodif))


            history = model.fit(np.array(x_train), np.array(y_train), nb_epoch=epochs, batch_size=batch, verbose =0)
            loss=np.mean(history.history['loss'])

            LOSS[0]=loss
            enregistrement()


            # ON ARRETE QUAND C BON
            if(COMPTEUR[0]==END):
                print("Fin de l'exécution !")
                os._exit(0)

        COMPTEUR[0]+=1
        "PRISE DE DECISION"
        if (end_condition(spots, next_head)):
            if(ratioSingle[0]>max(RATIOSSINGLE)):

                RATIOSSINGLE.append(ratioSingle[0])
                enregistrementModel(model)
            LOST[0]+=1
            return snake.tailmax




        if is_food(spots, next_head):
            FOUND[0]+=1
            ratioSingle[0] += 1
            snake.tailmax += 1
            food = find_food(spots)

        snake.deque.append(next_head)

        if len(snake.deque) > snake.tailmax:
            snake.deque.popleft()

        # Draw code
        if(IHM):
            screen.fill(BLACK)  # makes screen black

            spots = update_board(screen, [snake], food)

            pygame.display.update()
        else:
            spots = update_board(screen, [snake], food)




def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
                                      BOARD_LENGTH * OFFSET])
    pygame.display.set_caption("Snaake")
    thing = pygame.Rect(10, 10, 50, 50)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255, 255), pygame.Rect(50, 50, 10, 10))
    first = True

    playing = True
    while playing:
        if first or pick == 3:
            pick = 1

        options = {0: quit,
                   1: one_player}
        now = options[pick](screen)
        if now == False:
            break
        elif pick == 1 or pick == 2:
            eaten = now / 4 - 1
            "DECOMMENTER LA LIGNE D EN DESSOUS == OBTENIR DES ECRANS DE GAMEOVER ENTRE CHAQUE MORT"
            # playing = game_over(screen, eaten)
            first = False

    pygame.quit()


if __name__ == "__main__":
    main()
