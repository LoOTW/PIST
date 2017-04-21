"REMARQUES GENERALES : VARIABLES"
# la matrice coord == le corps du Snake
# la matrice spots == la plateau de jeu
from keras.optimizers import Adam

import SharedStatic

from Snake import Snake
from Static import BOARD_LENGTH, speed, OFFSET

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



WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)



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

class Board(object):
    def __init__(self, screen):
        self.screen = screen
        self.IHM=False
        self.BLACK = (0, 0, 0)

    "COLORATION ALEATOIRE SUPER SWAG DU SNAKE"


    def rand_color(self):
        return (random.randrange(254) | 64, random.randrange(254) | 64, random.randrange(254) | 64)





    'FONCTION PLACANT LA POPOMME'

    def find_food(self,spots):
        while True:
            food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
            if (not (spots[food[0]][food[1]] == 1 or
                             spots[food[0]][food[1]] == 2)):
                break
        return food


    'FONCTION TESTANT LES DEUX CONDITIONS DE GAMEOVER'

    def end_condition(self, board, coord):
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
    def make_board(self, ):

        return [[0 for i in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]


    "MAJ DU TABLEAU DE JEU"

    def update_board(self, snakes, food):
        if self.IHM:
            rect = pygame.Rect(0, 0, OFFSET, OFFSET)

            # redef du tableau de jeu case par case
            spots = [[] for i in range(BOARD_LENGTH)]
            num1 = 0
            num2 = 0
            for row in spots:
                for i in range(BOARD_LENGTH):
                    row.append(0)
                    temprect = rect.move(num1 * OFFSET, num2 * OFFSET)
                    pygame.draw.rect(self.screen, self.BLACK, temprect)
                    num2 += 1
                num1 += 1

            # ca place la popomme
            spots[food[0]][food[1]] = 2

            temprect = rect.move(food[1] * OFFSET, food[0] * OFFSET)
            pygame.draw.rect(self.screen, RED, temprect)

            # ca renseigne ou qu il est le snake
            for snake in snakes:
                for coord in snake.deque:
                    spots[coord[0]][coord[1]] = 1
                    temprect = rect.move(coord[1] * OFFSET, coord[0] * OFFSET)
                    pygame.draw.rect(self.screen, coord[2], temprect)
        else:
            spots = self.make_board()

            # ca place la popomme
            spots[food[0]][food[1]] = 2

            # ca renseigne ou qu il est le snake
            for snake in snakes:
                for coord in snake.deque:
                    spots[coord[0]][coord[1]] = 1
        return spots


    def get_color(self, s):
        if s == "bk":
            return self.BLACK
        elif s == "wh":
            return WHITE
        elif s == "rd":
            return RED
        elif s == "bl":
            return BLUE
        elif s == "fo":
            return self.rand_color()
        else:
            print("WHAT", s)
            return BLUE


    "I DON T KNOW REALLY LOL"

    def launchUpdate(self, spots, next_head, snake, food):
        if self.is_food(spots, next_head):
            SharedStatic.FOUND[0] += 1
            snake.tailmax += 4
            food = self.find_food(spots)

        snake.deque.append(next_head)

        if len(snake.deque) > snake.tailmax:
            snake.deque.popleft()

        # Draw code
        if self.IHM:
            self.screen.fill(self.BLACK)  # makes screen black

            spots = self.update_board([snake], food)

            pygame.display.update()
        else:
            spots = self.update_board([snake], food)

    def update_board_delta(self, deltas):
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
                addqueue.append((d[1], d[2], self.get_color(self, d[3])))

        for d_coord in delqueue:
            temprect = rect.move(d_coord[1] * OFFSET, d_coord[0] * OFFSET)
            # TODO generalize background color
            pygame.draw.rect(self.screen, self.BLACK, temprect)

        for a_coord in addqueue:
            temprect = rect.move(a_coord[1] * OFFSET, a_coord[0] * OFFSET)
            pygame.draw.rect(self.screen, a_coord[2], temprect)

        return change_list


    "DEF DU MENU DU SNAKE"


    # Return 0 to exit the program, 1 for a one-player game
    def menu(self):
        font = pygame.font.Font(None, 30)
        menu_message1 = font.render("Press enter for one-player, t for two-player", True, WHITE)
        menu_message2 = font.render("C'est le PIST de l'ambiance", True, WHITE)

        self.screen.fill(self.BLACK)
        self.screen.blit(menu_message1, (32, 32))
        self.screen.blit(menu_message2, (32, 64))
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


    def quit(self):
        return False


    "FAIT SE DEPLACER LE SNAKE SELON LE DEPLACEMENT INDIQUE DANS LA DEQUE NEXTDIR + SA DIRCTION ACTUELLE"


    def move(self, snake):
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


    def is_food(self, board, point):
        return board[point[0]][point[1]] == 2


    "EXP REPLAY"


    def end_cond(self, etat, action):
        if etat[len(etat) - 3] == '0' and action == 0:
            return True
        if etat[len(etat) - 2] == '0' and action == 1:
            return True
        if etat[len(etat) - 1] == '0' and action == 2:
            return True
        return False





    "VERSION UN JOUEUR"


    # Return false to quit program, true to go to
    # gameover screen
    def one_player(self, screen):
        spots = self.make_board()

        food = self.find_food(spots)
        snake = Snake()



        next_head = self.move(snake)
        "PRISE DE DECISION"
        SharedStatic.AGENT.joue(snake, food, spots, next_head)






    "DEINITION TABLEAU GAMEOVER"


    def game_over(self, screen, eaten):
        message1 = "You ate %d foods" % eaten
        message2 = "Press enter to play again, esc to quit."
        game_over_message1 = pygame.font.Font(None, 30).render(message1, True, self.BLACK)
        game_over_message2 = pygame.font.Font(None, 30).render(message2, True, self.BLACK)

        overlay = pygame.Surface((BOARD_LENGTH * OFFSET, BOARD_LENGTH * OFFSET))
        overlay.fill((84, 84, 84))
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))

        screen.blit(game_over_message1, (35, 35))
        screen.blit(game_over_message2, (65, 65))
        game_over_message1 = pygame.font.Font(None, 30).render(message1, True, WHITE)
        game_over_message2 = pygame.font.Font(None, 30).render(message2, True, WHITE)
        screen.blit(game_over_message1, (32, 32))
        screen.blit(game_over_message2, (62, 62))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key == pygame.K_RETURN:
                        return True


    def leaderboard(screen):
        font = pygame.font.Font(None, 30)
        screen.fill(BLACK)
        try:
            with open("leaderboard.txt") as f:
                lines = f.readlines()
                titlemessage = font.render("Leaderboard", True, WHITE)
                screen.blit(titlemessage, (32, 32))
                dist = 64
                for line in lines:
                    delimited = line.split(",")
                    delimited[1] = delimited[1].strip()
                    message = "{0[0]:.<10}{0[1]:.>10}".format(delimited)
                    rendered_message = font.render(message, True, WHITE)
                    screen.blit(rendered_message, (32, dist))
                    dist += 32
        except IOError:
            message = "Nothing on the leaderboard yet."
            rendered_message = font.render(message, True, WHITE)
            screen.blit(rendered_message, (32, 32))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key == pygame.K_RETURN:
                        return True


