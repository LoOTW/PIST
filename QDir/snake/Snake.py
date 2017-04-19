"DESCRIPTION CLASSE"
#classe Snake --> cree un serpent

import random
from collections import deque
from QDir.snake import Static

import numpy as np
class Snake(object):
    def __init__(self, direction=Static.DIRECTIONS.Right, point=(16, 16, Static.BLUE), color=None):
        # taille max sachant nb popommes mangees
        self.tailmax = 4

        # dir acuelle
        self.direction = direction

        # coord points du serpent (le dernier elem == tete)
        # ie head == self.deque[self.deque.__len__-1][self.deque.__len__-1]
        self.deque = deque()
        self.deque.append(point)

        # couleur (obviously)
        self.color = Static.BLUE

        # prochaine direction (je sais pas pourquoi il faut un deque et pas juste unelement ici en vrai)
        self.nextDir = deque()

        # etat Snake
        self.state = ""

        # exp replay
        self.experience = Static.EXP

        # politique decision
        self.Q = np.array([[0, 0, 0]])

    def get_color(self):
        return Static.BLUE

    "RETOURNE LA LISTE [voisin gauche, voisin devant, voisin droite]"

    def voisins(self, head):
        i = head[0]
        j = head[1]
        V = []

        if (self.direction == Static.DIRECTIONS.Up):
            V.append([i, j - 1])
            V.append([i - 1, j])
            V.append([i, j + 1])

        elif (self.direction == Static.DIRECTIONS.Right):
            V.append([i - 1, j])
            V.append([i, j + 1])
            V.append([i + 1, j])

        elif (self.direction == Static.DIRECTIONS.Down):
            V.append([i, j + 1])
            V.append([i + 1, j])
            V.append([i, j - 1])

        elif (self.direction == Static.DIRECTIONS.Left):
            V.append([i + 1, j])
            V.append([i, j - 1])
            V.append([i - 1, j])
        return V

    "donne actions possibles (directions relatives pour Snake) a partir de directions absolues (par rapport au plateau)"

    def trad_direction(self, nv_dir):
        if (self.direction == Static.DIRECTIONS.Up):
            if nv_dir == 0:
                return Static.DIRECTIONS.Left
            if nv_dir == 1:
                return Static.DIRECTIONS.Up
            else:
                return Static.DIRECTIONS.Right

        elif (self.direction == Static.DIRECTIONS.Right):
            if nv_dir == 0:
                return Static.DIRECTIONS.Up
            if nv_dir == 1:
                return Static.DIRECTIONS.Right
            else:
                return Static.DIRECTIONS.Down

        elif (self.direction == Static.DIRECTIONS.Down):
            if nv_dir == 0:
                return Static.DIRECTIONS.Right
            if nv_dir == 1:
                return Static.DIRECTIONS.Down
            else:
                return Static.DIRECTIONS.Left

        elif (self.direction == Static.DIRECTIONS.Left):
            if nv_dir == 0:
                return Static.DIRECTIONS.Down
            if nv_dir == 1:
                return Static.DIRECTIONS.Left
            else:
                return Static.DIRECTIONS.Up

    # choix prochaine direction
    def populate_nextDir(self, events, identifier):
        "Code pour direction automatique du serpent"
        aleat = random.randrange(0, 3)
        tirage = random.random()

        "Cas ou le serpent explore --> direction aleat"
        if Static.EPS[0] > Static.EPS[1]:
            Static.EPS[0] -= Static.EPSSTEPS

        if tirage < Static.EPS[0]:
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
