import pygame

from Agent import Agent
from Board import Board
from Static import BOARD_LENGTH, OFFSET
def init():
    global screen
    global board
    global AGENT
    global PASAVANTMORT
    global LOSS
    global LOSSES
    global DEFEATS
    global VICTORIES
    global RATIOS
    global FOUND
    global LOST
    global PAS
    global EXP
    global EPSILONS
    EPSILONS = []
    EXP = []

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
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
                                      BOARD_LENGTH * OFFSET])
    board = Board(screen)

    AGENT = Agent(board)
