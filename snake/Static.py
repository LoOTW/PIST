"REMARQUES GENERALES : VARIABLES"
# la matrice coord == le corps du Snake
# la matrice spots == la plateau de jeu
from keras.optimizers import Adam

"Importation modules utiles"
from collections import deque, namedtuple
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
NB_NEURONES=4
NB_COUCHES=1

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
    model.add(Dense(input_dim=5, output_dim=3))
    for i in range(NB_COUCHES):
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

#INTERMEDIAIRES DE CALCULS
LOSS=[0]
FOUND=[0]
LOST=[0]
PAS=[0]



IHM=True
speed = 5000
BOARD_LENGTH = 32
OFFSET = 16
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
EXP = []

COMPTEUR = [0]


DIRECTIONS = namedtuple('DIRECTIONS',
                        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)
