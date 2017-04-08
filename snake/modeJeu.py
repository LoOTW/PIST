"DESCRIPTION CLASSE"
#

import pygame

import numpy as np
import random
import os
from snake.Jeu import Jeu
from snake.Static import *


class ModeJeu(object):
    def __init__(self, e):
        self.ecran = e
        
    def mode(self,indice):
        if indice == 0:
            return self.quit
        elif indice == 1:
            return self.one_player
        
    "LANCE LE JEU (UN JOUEUR)"    
    # Return false to quit program, true to go to gameover screen
    def one_player(self):
        screen = self.ecran
        clock = pygame.time.Clock()
        #spots = make_board()
        spots = [[0 for i in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]
        jeu = Jeu()
        
        food = jeu.find_food(spots)
        snake = jeu.s[0]
        currentHead = snake.deque[snake.deque.__len__() - 1]
        snake.state = jeu.code_etat(currentHead, snake.voisins(currentHead), food, spots)
    
        while True:
            clock.tick(speed)
            "Event processing"
            done = False
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    print("Quit given")
                    done = True
                    break
            if done:
                return False
    
            "Stockage en memoire de la transition (s,a,r,s') qui vient d etre effectuee"
            old_state = snake.state
            lenOldState=len(old_state)
            oldStateSplit = old_state.split("_")
            temp=model.predict(np.array([[oldStateSplit[0], oldStateSplit[1], old_state[lenOldState - 3],
                                          old_state[lenOldState - 2], old_state[lenOldState - 1]]]))
           
            snake.Q=np.array([temp[0][0],temp[0][1],temp[0][2]])
            next_head = jeu.move()
            snake.populate_nextDir(events, "arrows")
            snake.state = jeu.code_etat(next_head, snake.voisins(next_head), food, spots)
            directionRelative = snake.trad_direction(snake.direction)
            recomp = jeu.get_reward(old_state, directionRelative)
            snake.experience.append(
                [old_state, directionRelative, recomp, snake.state])
    
            "On garantit que le nb de transitions stockees reste borne"
            if (len(snake.experience) > lenExpMax):
                snake.experience.pop(random.randrange(lenExpMax))
    
            "Exp replay"
            PAS[0]+=1
            "On rassemble des transitions stockees en memoire qui vont servir a l apprentissage"
            if(COMPTEUR[0]%step==0 and COMPTEUR[0]!=0):
                x_train=[]
                y_train=[]
                lenExp = len(snake.experience)
                if (lenExp >= batch):
    
                    for i in range(samplesSize):
                        sample = random.choice(snake.experience) #une transion (s,a,r,s)
                        sample0 = sample[0] #s l etat de depart
                        sample1 = sample[1] #a la direction prise
                        sample2 = sample[2] #r la recompense pour l etat apres realisaion de a depuis s
                        sample3 = sample[3] #s' l etat apres realisation de a depuis s
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
                        if jeu.end_cond(sample0, sample1):
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
                
                "on apprend"
                history = model.fit(np.array(x_train), np.array(y_train), nb_epoch=epochs, batch_size=batch, verbose =0)
                loss=np.mean(history.history['loss'])
    
                LOSS[0]=loss
    
                jeu.enregistrement(model)
    
                # ON ARRETE QUAND C EST BON
                if(loss<1 or COMPTEUR[0]==END):
                    print("Fin de l'exécution !")
                    os._exit(0)
    
            COMPTEUR[0]+=1
                    
            "rise de decision (basee sur Q)"
            if (jeu.end_condition(spots, next_head)):
                LOST[0]+=1
                return snake.tailmax
    
            if spots[next_head[0]][next_head[1]] == 2:
                FOUND[0]+=1
                snake.tailmax += 4
                food = jeu.find_food(spots)
    
            snake.deque.append(next_head)
    
            if len(snake.deque) > snake.tailmax:
                snake.deque.popleft()
    
            # Draw code
            if(IHM):
                screen.fill(BLACK)  # makes screen black
    
                spots = jeu.update_board(screen, food)
    
                pygame.display.update()
            else:
                spots = jeu.update_board(screen, food)
                
    "DEF DU MENU DU SNAKE"
    # Return 0 to exit the program, 1 for a one-player game
    def menu(self):
        screen = self.ecran
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
    #                if event.key == pygame.K_t:
    #                    return 2
    #                if event.key == pygame.K_l:
    #                    return 3
    #                if event.key == pygame.K_n:
    #                    return 4
            if done:
                break
        if done:
            pygame.quit()
            return 0
    
    "CAS OU L UTILISATEUR CLIQUE SUR LA CROIX DE LA FENETRE"
    def quit(self):
        return False