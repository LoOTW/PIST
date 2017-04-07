
import random
import numpy as np
import os
from collections import deque

import pygame

from snake.Snake import Snake
from snake.Static import BOARD_LENGTH, IHM, OFFSET, BLACK, RED, WHITE, BLUE, DIRECTIONS, LOSS, PAS, VICTORIES, LOSSES, \
    PASAVANTMORT, FOUND, DEFEATS, LOST, RATIOS, EPSILONS, EPS, COMPTEUR, step, speed, model, lenExpMax, batch, \
    samplesSize, GAMMA, epochs, END

"COLORATION ALEATOIRE SUPER SWAG DU SNAKE"


def rand_color():
    return (random.randrange(254) | 64, random.randrange(254) | 64, random.randrange(254) | 64)


"ASSOCIE A TOUT ETAT POSSIBLE UN CODE UNIQUE (A PARTIR DES LA POSITION + ETAT VOISINS"

# "['case qui tue','case vide','case pomme']  = [0,1,2]
def code_etat(position, voisins, food, spots):
    s = ""
    #print("Je suis en " + str(position))
    #print("Mes voisins sont : " + str(voisins))
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
   #print("Mon état est donc " +str(s))
    return s

"'CREATION CLASSE SNAKE"


# demarre initialement au milieu du board ie aux coordonnees (16,16), en se dirigeant vers la droite
# remarque : deque == type d'objet (en gros une liste chainee)



'FONCTION PLACANT LA POPOMME'

def find_food(spots):
    while True:
        food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[food[0]][food[1]] == 1 or
                         spots[food[0]][food[1]] == 2)):
            break
    return food


'FONCTION TESTANT LES DEUX CONDITIONS DE GAMEOVER'

def end_condition(board, coord):
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
def make_board():

    return [[0 for i in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]

"FONCTION RETOURNANT LA RECOMPENSE POUR UNE ACTION"

def get_reward(old_state, directionRelative):
    tete = int(old_state[len(old_state)-1-(2-directionRelative)])
    if(tete<32 and tete>=0 and tete<32 and tete>=0):
        #print(tete[0])
        #print(tete[1])
        if tete == 0:
            return -20
        elif tete== 1:
            return -1
        elif tete ==2:
            return 50
    else:
        return -20

"MAJ DU TABLEAU DE JEU"

def update_board(screen, snakes, food):
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
        spots = make_board()

        # ca place la popomme
        spots[food[0]][food[1]] = 2

        # ca renseigne ou qu il est le snake
        for snake in snakes:
            for coord in snake.deque:
                spots[coord[0]][coord[1]] = 1
    return spots


def get_color(s):
    if s == "bk":
        return BLACK
    elif s == "wh":
        return WHITE
    elif s == "rd":
        return RED
    elif s == "bl":
        return BLUE
    elif s == "fo":
        return rand_color()
    else:
        print("WHAT", s)
        return BLUE


"I DON T KNOW REALLY LOL"


def update_board_delta(screen, deltas):
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
            addqueue.append((d[1], d[2], get_color(d[3])))

    for d_coord in delqueue:
        temprect = rect.move(d_coord[1] * OFFSET, d_coord[0] * OFFSET)
        # TODO generalize background color
        pygame.draw.rect(screen, BLACK, temprect)

    for a_coord in addqueue:
        temprect = rect.move(a_coord[1] * OFFSET, a_coord[0] * OFFSET)
        pygame.draw.rect(screen, a_coord[2], temprect)

    return change_list


"DEF DU MENU DU SNAKE"


# Return 0 to exit the program, 1 for a one-player game
def menu(screen):
    font = pygame.font.Font(None, 30)
    menu_message1 = font.render("Press enter for one-player, t for two-player", True, WHITE)
    menu_message2 = font.render("C'est le PIST de l'ambiance", True, WHITE)

    screen.fill(BLACK)
    screen.blit(menu_message1, (32, 32))
    screen.blit(menu_message2, (32, 64))
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


def quit(screen):
    return False


"FAIT SE DEPLACER LE SNAKE SELON LE DEPLACEMENT INDIQUE DANS LA DEQUE NEXTDIR + SA DIRCTION ACTUELLE"


def move(snake):
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


def is_food(board, point):
    return board[point[0]][point[1]] == 2


"EXP REPLAY"


def end_cond(etat, action):
    if etat[len(etat) - 3] == '0' and action == 0:
        return True
    if etat[len(etat) - 2] == '0' and action == 1:
        return True
    if etat[len(etat) - 1] == '0' and action == 2:
        return True
    return False


def enregistrement(m):

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

    saveOnDisk("loss", LOSSES)
    saveOnDisk("epsilon",EPSILONS)
    saveOnDisk("victoires",VICTORIES)
    saveOnDisk("defaites", DEFEATS)
    saveOnDisk("ratios",RATIOS)
    saveOnDisk("pasAvantMort", PASAVANTMORT)
    LOST[0] = 0
    FOUND[0] = 0
    PAS[0]=0

def saveOnDisk(nomDuFichier, liste):
    with open(nomDuFichier+".txt", "w") as file:
        file.write(str(liste))


"VERSION UN JOUEUR"


# Return false to quit program, true to go to
# gameover screen
def one_player(screen):
    clock = pygame.time.Clock()
    spots = make_board()

    food = find_food(spots)
    snake = Snake()
    currentHead = snake.deque[snake.deque.__len__() - 1]
    snake.state = code_etat(currentHead, snake.voisins(currentHead), food, spots)
    #snake.rewardMatrix = snake.initializeRewardMatrix(food)

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
        lenOldState=len(old_state)
        oldStateSplit = old_state.split("_")
        temp=model.predict(np.array([[oldStateSplit[0], oldStateSplit[1], old_state[lenOldState - 3],
                                      old_state[lenOldState - 2], old_state[lenOldState - 1]]]))
        snake.Q=np.array([temp[0][0],temp[0][1],temp[0][2]])

        next_head = move(snake)
        snake.populate_nextDir(events, "arrows")
        snake.state = code_etat(next_head, snake.voisins(next_head), food, spots)

        #new_state = snake.state

        "EXP REPLAY"
        directionRelative = snake.trad_direction(snake.direction)
        recomp = get_reward(old_state, directionRelative)

        snake.experience.append(
            [old_state, directionRelative, recomp, snake.state])


        if (len(snake.experience) > lenExpMax):
            snake.experience.pop(random.randrange(lenExpMax))

        PAS[0]+=1
        if(COMPTEUR[0]%step==0 and COMPTEUR[0]!=0):
            x_train=[]
            y_train=[]
            lenExp = len(snake.experience)
            if (lenExp >= batch):

                for i in range(samplesSize):
                    sample = random.choice(snake.experience)
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
                    #print(Qmodif)
                    if end_cond(sample0, sample1):
                        Qmodif[0][sample1] = np.array([[sample2]])
                    else:
                        Qmodif[0][sample1] = np.array(sample2 + GAMMA * temp2.max())
                    x_train.append(oldState4Keras)
                    y_train.append([Qmodif[0][0], Qmodif[0][1], Qmodif[0][2]])
                    #print("on ajoute "+str(sample2 + GAMMA * (temp2.max() - Qmodif[0][sample1])))
                    #print("L'état est " + str(sample0)+" La direction choisie est " + str(sample1))
                    #print("L'état suivant est " + str(sample3))
                    #print("La récompense est " + str(sample2))
                    #print(Qmodif)

            history = model.fit(np.array(x_train), np.array(y_train), nb_epoch=epochs, batch_size=batch, verbose =0)
            loss=np.mean(history.history['loss'])

            LOSS[0]=loss

            enregistrement(model)

            # ON ARRETE QUAND C BON
            if(loss<1 or COMPTEUR[0]==END):
                print("Fin de l'exécution !")
                os._exit(0)

        COMPTEUR[0]+=1
        "PRISE DE DECISION"
        if (end_condition(spots, next_head)):

            LOST[0]+=1
            return snake.tailmax




        if is_food(spots, next_head):
            FOUND[0]+=1
            snake.tailmax += 4
            food = find_food(spots)

        snake.deque.append(next_head)

        if len(snake.deque) > snake.tailmax:
            snake.deque.popleft()

        # Draw code
        if(IHM):
            screen.fill(BLACK)  # makes screen black

            spots = update_board(screen, [snake], food)

            pygame.display.update()
        else:
            spots = update_board(screen, [snake], food)


"DEINITION TABLEAU GAMEOVER"


def game_over(screen, eaten):
    message1 = "You ate %d foods" % eaten
    message2 = "Press enter to play again, esc to quit."
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, BLACK)
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, BLACK)

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


def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
                                      BOARD_LENGTH * OFFSET])
    pygame.display.set_caption("Snaake")
    thing = pygame.Rect(10, 10, 50, 50)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255, 255), pygame.Rect(50, 50, 10, 10))
    first = True
    playing = True
    while playing:
        if first or pick == 3:
            pick = menu(screen)

        options = {0: quit,
                   1: one_player,
                   3: leaderboard,
                    }
        now = options[pick](screen)
        if now == False:
            break
        elif pick == 1 or pick == 2:
            eaten = now / 4 - 1
            "DECOMMENTER LA LIGNE D EN DESSOUS == OBTENIR DES ECRANS DE GAMEOVER ENTRE CHAQUE MORT"
            # playing = game_over(screen, eaten)
            first = False

    pygame.quit()


if __name__ == "__main__":
    main()