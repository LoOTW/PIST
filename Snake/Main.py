import pygame

import SharedStatic
from Board import Board
from Static import BOARD_LENGTH, OFFSET
SharedStatic.init()
pygame.init()


pygame.display.set_caption("Snaake")
thing = pygame.Rect(10, 10, 50, 50)
pygame.draw.rect(SharedStatic.AGENT.board.screen, pygame.Color(255, 255, 255, 255), pygame.Rect(50, 50, 10, 10))
first = True

playing = True
while playing:
    if first or pick == 3:
        pick = 1

    options = {0: quit,
               1: SharedStatic.AGENT.board.one_player,
               3: SharedStatic.AGENT.board.leaderboard}
    now = SharedStatic.AGENT.board.one_player(SharedStatic.AGENT.board.screen)

    if now == False:
        break
    elif pick == 1 or pick == 2:
        "DECOMMENTER LA LIGNE D EN DESSOUS == OBTENIR DES ECRANS DE GAMEOVER ENTRE CHAQUE MORT"
        # playing = game_over(screen, eaten)
        first = False

pygame.quit()

