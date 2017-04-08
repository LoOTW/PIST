"DESCRIPTION CLASSE"
#classe Jeu --> cree une instance de jeu (rassemble les methodes propres a la dynamique du jeu)

import random
import pygame

from snake.Snake import Snake
from snake.Static import *

class Jeu(object):
    def __init__(self):
        self.s = [Snake()]
        
    "ASSOCIE A TOUT ETAT POSSIBLE UN CODE UNIQUE (A PARTIR DES LA POSITION + ETAT VOISINS)"
    "['case qui tue','case vide','case pomme']  = [0,1,2]"
    
    def code_etat(self, position, voisins, food, spots):
        s = ""
        #print("Je suis en " + str(position))
        #print("Mes voisins sont : " + str(voisins))
        
        "Distance selon les les x"
        s += str(position[0] - food[0]) + "_"
    
        "Selon les y"
        s += str(position[1] - food[1])
    
        "Obtention etats cases voisines"
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
    
    'FONCTION PLACANT LA POPOMME'
    def find_food(self, spots):
        while True:
            food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
            if (not (spots[food[0]][food[1]] == 1 or
                             spots[food[0]][food[1]] == 2)):
                break
        return food
    
    
    'FONCTION TESTANT LES DEUX CONDITIONS DE GAMEOVER'
    
    def end_condition(self,board, coord):
        # teste si le Snake vient de se manger salement le mur
        if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or
                    coord[1] >= BOARD_LENGTH):
            return True
        # teste si le Snake vient de se manger stupidement la queue
        if (board[coord[0]][coord[1]] == 1):
            return True
        return False
    
    def make_board(self):
        return [[0 for i in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]
    
    "FONCTION RETOURNANT LA RECOMPENSE POUR UNE ACTION"
    
    def get_reward(self, old_state, directionRelative):
        tete = int(old_state[len(old_state)-1-(2-directionRelative)])
        if(tete<32 and tete>=0 and tete<32 and tete>=0):
            if tete == 0:
                return -20
            elif tete== 1:
                return -1
            elif tete ==2:
                return 50
        else:
            return -20
    
    "MAJ DU TABLEAU DE JEU"
    
    def update_board(self, screen, food):
        snakes = self.s
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
            spots = self.make_board()
            # ca place la popomme
            spots[food[0]][food[1]] = 2
    
            # ca renseigne ou qu il est le snake
            for snake in snakes:
                for coord in snake.deque:
                    spots[coord[0]][coord[1]] = 1
        return spots

    def move(self):
        snake = self.s[0]
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
    
    "EXP REPLAY"
    
    def end_cond(self, etat, action):
        if etat[len(etat) - 3] == '0' and action == 0:
            return True
        if etat[len(etat) - 2] == '0' and action == 1:
            return True
        if etat[len(etat) - 1] == '0' and action == 2:
            return True
        return False
    
    
    def enregistrement(self, m):
    
        model_json = m.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        m.save_weights("model.h5")
    
        PASAVANTMORT.append(LOSS[0]/PAS[0])
        LOSSES.append(LOSS[0])
        VICTORIES.append(FOUND[0])
        DEFEATS.append(LOST[0])
        RATIOS.append(FOUND[0] / (LOST[0] + 1))
        EPSILONS.append(EPS[0])
    
    
    
        print("Victoire : " + str(FOUND[0]) + " Défaites : " + str(LOST[0]) + " Ratio : " + str(FOUND[0] / (LOST[0] + 1))
              + " EPS : " + str(EPS[0]) + " LOSS : " + str(LOSS[0])+" ITERATIONS : "+str(COMPTEUR[0]/step))
    
        open("loss"+".txt", "w").write(str(LOSSES))
        open("epsilon"+".txt", "w").write(str(EPSILONS))
        open("victoires"+".txt", "w").write(str(VICTORIES))
        open("defaites"+".txt", "w").write(str(DEFEATS))
        open("ratios"+".txt", "w").write(str(RATIOS))
        open("pasAvantMort"+".txt", "w").write(str(PASAVANTMORT))
        
        LOST[0] = 0
        FOUND[0] = 0
        PAS[0]=0   
