"DESCRIPTION CLASSE"
#classe Jeu --> cree une instance de jeu (rassemble les methodes propres a la dynamique du jeu)

import random
import pygame

from .Snake import Snake
from QDir.snake import Static

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
            if (v[0] < 0 or v[0] >= Static.BOARD_LENGTH or v[1] < 0 or v[1] >= Static.BOARD_LENGTH):
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
            food = random.randrange(Static.BOARD_LENGTH), random.randrange(Static.BOARD_LENGTH)
            if (not (spots[food[0]][food[1]] == 1 or
                             spots[food[0]][food[1]] == 2)):
                break
        return food


    'FONCTION TESTANT LES DEUX CONDITIONS DE GAMEOVER'

    def end_condition(self,board, coord):
        # teste si le Snake vient de se manger salement le mur
        if (coord[0] < 0 or coord[0] >= Static.BOARD_LENGTH or coord[1] < 0 or
                    coord[1] >= Static.BOARD_LENGTH):
            return True
        # teste si le Snake vient de se manger stupidement la queue
        if (board[coord[0]][coord[1]] == 1):
            return True
        return False

    def make_board(self):
        return [[0 for i in range(Static.BOARD_LENGTH)] for i in range(Static.BOARD_LENGTH)]

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
        if Static.IHM:
            rect = pygame.Rect(0, 0, Static.OFFSET, Static.OFFSET)

            # redef du tableau de jeu case par case
            spots = [[] for i in range(Static.BOARD_LENGTH)]
            num1 = 0
            num2 = 0
            for row in spots:
                for i in range(Static.BOARD_LENGTH):
                    row.append(0)
                    temprect = rect.move(num1 * Static.OFFSET, num2 * Static.OFFSET)
                    pygame.draw.rect(screen, Static.BLACK, temprect)
                    num2 += 1
                num1 += 1

            # ca place la popomme
            spots[food[0]][food[1]] = 2

            temprect = rect.move(food[1] * Static.OFFSET, food[0] * Static.OFFSET)
            pygame.draw.rect(screen, Static.RED, temprect)

            # ca renseigne ou qu il est le snake
            for snake in snakes:
                for coord in snake.deque:
                    spots[coord[0]][coord[1]] = 1
                    temprect = rect.move(coord[1] * Static.OFFSET, coord[0] * Static.OFFSET)
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

        if (next_dir == Static.DIRECTIONS.Up):
            if snake.direction != Static.DIRECTIONS.Down:
                next_move = (head[0] - 1, head[1], snake.get_color())
                snake.direction = next_dir
            else:
                next_move = (head[0] + 1, head[1], snake.get_color())
        elif (next_dir == Static.DIRECTIONS.Down):
            if snake.direction != Static.DIRECTIONS.Up:
                next_move = (head[0] + 1, head[1], snake.get_color())
                snake.direction = next_dir
            else:
                next_move = (head[0] - 1, head[1], snake.get_color())
        elif (next_dir == Static.DIRECTIONS.Left):
            if snake.direction != Static.DIRECTIONS.Right:
                next_move = (head[0], head[1] - 1, snake.get_color())
                snake.direction = next_dir
            else:
                next_move = (head[0], head[1] + 1, snake.get_color())
        elif (next_dir == Static.DIRECTIONS.Right):
            if snake.direction != Static.DIRECTIONS.Left:
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

        Static.PASAVANTMORT.append(Static.LOSS[0]/Static.PAS[0])
        Static.LOSSES.append(Static.LOSS[0])
        Static.VICTORIES.append(Static.FOUND[0])
        Static.DEFEATS.append(Static.LOST[0])
        Static.RATIOS.append(Static.FOUND[0] / (Static.LOST[0] + 1))
        Static.EPSILONS.append(Static.EPS[0])



        print("Victoire : " + str(Static.FOUND[0]) + " Défaites : " + str(Static.LOST[0]) + " Ratio : " + str(Static.FOUND[0] / (Static.LOST[0] + 1))
              + " Static.EPS : " + str(Static.EPS[0]) + " Static.LOSS : " + str(Static.LOSS[0])+" ITERATIONS : "+str(Static.COMPTEUR[0]/Static.step))

        open("loss"+".txt", "w").write(str(Static.LOSSES))
        open("epsilon"+".txt", "w").write(str(Static.EPSILONS))
        open("victoires"+".txt", "w").write(str(Static.VICTORIES))
        open("defaites"+".txt", "w").write(str(Static.DEFEATS))
        open("ratios"+".txt", "w").write(str(Static.RATIOS))
        open("pasAvantMort"+".txt", "w").write(str(Static.PASAVANTMORT))

        Static.LOST[0] = 0
        Static.FOUND[0] = 0
        Static.PAS[0]=0