"SCRIPT DU MAIN (a executer pour lancer le jeu)"

import pygame
from Static import BOARD_LENGTH, OFFSET
from modeJeu import ModeJeu

def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
                                      BOARD_LENGTH * OFFSET])
    modeJeu = ModeJeu(screen)
    pygame.display.set_caption("Snake")
    #thing = pygame.Rect(10, 10, 50, 50)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255, 255), pygame.Rect(50, 50, 10, 10))
    first = True
    #playing = True
    
    while True:
        if first:
            pick = modeJeu.menu()

        now = modeJeu.mode(pick)()
        
        if now == False:
            break
        if pick == 1:
            #eaten = now / 4 - 1
            # playing = game_over(screen, eaten)
            first = False

    pygame.quit()


if __name__ == "__main__":
    main()