import sys
from collections import deque
from pathlib import Path
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers import Dense
import os
import random
import pygame
import socket
import select
import numpy as np
from pathlib import Path

from keras.optimizers import Adam

import SharedStatic
from Board import Board

COMPTEUR = [0]


#INPUTS DE TEST
from Static import BOARD_LENGTH, speed, clock
EXP = []

step=10000
END=500*step
EPS = [0.8, 0.05]
EPSSTEPS=(EPS[0]-EPS[1])/(END/2)
ALPHA=0.1
GAMMA=0.9
lenExpMax = 300000
samplesSize = 32000
batch = 32
epochs=10
#S'il n'y a qu'une seule couche le deuxième chiffre n'est pas pris en compte
NB_NEURONES=[4,4]
#IMPOOOOOOORTANT
NB_COUCHES=2






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
    model.add(Dense(input_dim=5, units=3))
    for i in range(NB_COUCHES):
        model.add(Dense(NB_NEURONES[i], activation='relu'))
    model.add(Dense(3))
optimizer=Adam(lr=ALPHA)
model.compile(loss='mse', optimizer=optimizer)


class Agent(object):

    def __init__(self, board):
        # etat Snake
        self.state = ""
        # mat recompense
        # self.rewardMatrix = [[] for i in range(BOARD_LENGTH + 2)]



        # politique decision
        self.Q = np.array([[0, 0, 0]])
        self.board = board

    def enregistrement(self, m):

        model_json = m.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        m.save_weights("model.h5")

        SharedStatic.PASAVANTMORT.append(SharedStatic.PAS[0] / (SharedStatic.LOST[0] + 1))
        SharedStatic.LOSSES.append(SharedStatic.LOSS[0])
        SharedStatic.VICTORIES.append(SharedStatic.FOUND[0])
        SharedStatic.DEFEATS.append(SharedStatic.LOST[0])
        SharedStatic.RATIOS.append(SharedStatic.FOUND[0] / (SharedStatic.LOST[0] + 1))
        SharedStatic.EPSILONS.append(EPS[0])

        print(
            "Victoire : " + str(SharedStatic.FOUND[0]) + " Défaites : " + str(SharedStatic.LOST[0]) + " Ratio : " + str(SharedStatic.FOUND[0] / (SharedStatic.LOST[0] + 1))
            + " EPS : " + str(EPS[0]) + " LOSS : " + str(SharedStatic.LOSS[0]) + " ITERATIONS : " + str(COMPTEUR[0] / step))

        self.saveOnDisk("loss", SharedStatic.LOSSES)
        self.saveOnDisk("epsilon", SharedStatic.EPSILONS)
        self.saveOnDisk("victoires", SharedStatic.VICTORIES)
        self.saveOnDisk("defaites", SharedStatic.DEFEATS)
        self.saveOnDisk("ratios", SharedStatic.RATIOS)
        self.saveOnDisk("pasAvantMort", SharedStatic.PASAVANTMORT)
        SharedStatic.LOST[0] = 0
        SharedStatic.FOUND[0] = 0
        SharedStatic.PAS[0] = 0

    def saveOnDisk(self, nomDuFichier, liste):
        with open(nomDuFichier + ".txt", "w") as file:
            file.write(str(liste))

    "FONCTION RETOURNANT LA RECOMPENSE POUR UNE ACTION"
    "ASSOCIE A TOUT ETAT POSSIBLE UN CODE UNIQUE (A PARTIR DES LA POSITION + ETAT VOISINS"

    # "['case qui tue','case vide','case pomme']  = [0,1,2]
    def code_etat(self, position, voisins, food, spots):
        s = ""
        # print("Je suis en " + str(position))
        # print("Mes voisins sont : " + str(voisins))
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
                    # print("Mon état est donc " +str(s))
        return s

    def get_reward(self, old_state, directionRelative):
        tete = int(old_state[len(old_state) - 1 - (2 - directionRelative)])
        if (tete < 32 and tete >= 0 and tete < 32 and tete >= 0):
            # print(tete[0])
            # print(tete[1])
            if tete == 0:
                return -20
            elif tete == 1:
                return -1
            elif tete == 2:
                return 50
        else:
            return -20
    # choix prochaine direction
    def decide(self):
        "Code pour direction automatique du serpent"
        aleat = random.randrange(0, 3)
        tirage = random.random()

        "Cas ou le serpent explore --> direction aleat"
        if EPS[0] > EPS[1]:
            EPS[0] -= EPSSTEPS

        if tirage < EPS[0]:

            return aleat

        # Cas ou le serpent exploite la politique de decision d action du QLearning
        else:

            if self.Q.argmax() == 0:
                return 0
            elif self.Q.argmax() == 1:
                return 1
            else:
                return 2

    def joue(self, snake, food, spots, next_head):
        currentHead = snake.deque[snake.deque.__len__() - 1]

        snake.state = self.code_etat(currentHead, snake.voisins(currentHead), food, spots)
        # snake.rewardMatrix = snake.initializeRewardMatrix(food)
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
            lenOldState = len(old_state)
            oldStateSplit = old_state.split("_")
            temp = model.predict(np.array([[oldStateSplit[0], oldStateSplit[1], old_state[lenOldState - 3],
                                            old_state[lenOldState - 2], old_state[lenOldState - 1]]]))
            snake.Q = np.array([temp[0][0], temp[0][1], temp[0][2]])


            snake.populate_nextDir(events, "arrows")
            snake.state = self.code_etat(next_head, snake.voisins(next_head), food, spots)

            # new_state = snake.state

            "EXP REPLAY"
            directionRelative = snake.trad_direction(snake.direction)
            recomp = self.get_reward(old_state, directionRelative)

            SharedStatic.EXP.append(
                [old_state, directionRelative, recomp, snake.state])

            if (len(SharedStatic.EXP) > lenExpMax):
                SharedStatic.EXP.pop(random.randrange(lenExpMax))

            SharedStatic.PAS[0] += 1
            if (COMPTEUR[0] % step == 0 and COMPTEUR[0] != 0):
                x_train = []
                y_train = []
                lenExp = len(SharedStatic.EXP)
                if (lenExp >= batch):

                    for i in range(samplesSize):
                        sample = random.choice(SharedStatic.EXP)
                        sample0 = sample[0]
                        sample1 = sample[1]
                        sample2 = sample[2]
                        sample3 = sample[3]
                        lenSample0 = len(sample0)
                        lenSample3 = len(sample3)

                        sample0split = sample[0].split("_")
                        sample3split = sample[3].split("_")
                        oldState4Keras = [sample0split[0], sample0split[1],
                                          sample0[lenSample0 - 3], sample0[lenSample0 - 2],
                                          sample0[lenSample0 - 1]]
                        Qmodif = model.predict(np.array([oldState4Keras]))
                        temp2 = model.predict(np.array([[sample3split[0], sample3split[1],
                                                         sample3[lenSample3 - 3], sample3[lenSample3 - 2],
                                                         sample3[lenSample3 - 1]]]))
                        # print(Qmodif)
                        if self.board.end_cond(sample0, sample1):
                            Qmodif[0][sample1] = np.array([[sample2]])
                        else:
                            Qmodif[0][sample1] = np.array(sample2 + GAMMA * temp2.max())
                        x_train.append(oldState4Keras)
                        y_train.append([Qmodif[0][0], Qmodif[0][1], Qmodif[0][2]])
                        # print("on ajoute "+str(sample2 + GAMMA * (temp2.max() - Qmodif[0][sample1])))
                        # print("L'état est " + str(sample0)+" La direction choisie est " + str(sample1))
                        # print("L'état suivant est " + str(sample3))
                        # print("La récompense est " + str(sample2))
                        # print(Qmodif)

                history = model.fit(np.array(x_train), np.array(y_train), epochs=epochs, batch_size=batch, verbose=0)
                loss = np.mean(history.history['loss'])

                SharedStatic.LOSS[0] = loss

                self.enregistrement(model)

                # ON ARRETE QUAND C BON
                if (loss < 1 or COMPTEUR[0] == END):
                    print("Fin de l'exécution !")
                    os._exit(0)
            COMPTEUR[0] += 1

            if (self.board.end_condition(spots, next_head)):
                SharedStatic.LOST[0] += 1
                return snake.tailmax
            self.board.launchUpdate(spots, next_head, snake, food)

