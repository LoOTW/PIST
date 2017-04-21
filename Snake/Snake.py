"REMARQUES GENERALES : VARIABLES"
# la matrice coord == le corps du Snake
# la matrice spots == la plateau de jeu
from keras.optimizers import Adam

import SharedStatic
from Static import BOARD_LENGTH

"Importation modules utiles"
from collections import deque, namedtuple
import sys
import os
import random
import pygame
import socket
import select
import numpy as np
from pathlib import Path


'DEF DES CARACTERISTIQ' \
'UES DU JEU'
# vitesse du Snake


IHM=False
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
EXP = []



DIRECTIONS = namedtuple('DIRECTIONS',
                        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)


"'CREATION CLASSE SNAKE"


# demarre initialement au milieu du board ie aux coordonnees (16,16), en se dirigeant vers la droite
# remarque : deque == type d'objet (en gros une liste chainee)

class Snake(object):
    def __init__(self, direction=DIRECTIONS.Right, point=(16, 16, BLUE), color=None):
        # taille max sachant nb popommes mangees
        self.tailmax = 4
        # prochaine direction (je sais pas pourquoi il faut un deque et pas juste unelement ici en vrai)
        self.nextDir = deque()
        # dir acuelle
        self.direction = direction

        # coord points du serpent (le dernier elem == tete)
        # ie head == self.deque[self.deque.__len__-1][self.deque.__len__-1]
        self.deque = deque()
        self.deque.append(point)

        # couleur (obviously)
        self.color = BLUE

    # choix prochaine direction
    def populate_nextDir(self, events, identifier):
        self.nextDir.appendleft(self.trad_direction(SharedStatic.AGENT.decide()))

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

