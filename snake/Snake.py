"DESCRIPTION CLASSE"
#classe Snake --> cree un serpent

import random
from collections import deque

from Static import DIRECTIONS, BLUE, EXP, EPS, EPSSTEPS

import numpy as np
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
