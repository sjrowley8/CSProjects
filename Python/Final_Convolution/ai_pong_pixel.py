"""
Ryan Grant, Michael Holt, Mitch Olson, Stephen Rowley
CSCI 315
Final Project
ai_pong_pixel.py
This program allows one user to play pong against an AI Paddle.
"""

import pygame
import pickle
import numpy as np
from dumpimage import dumpimage
from lenet5_pong import *

testing_input = []
have_new_input = False
SCR_WID = 960
SCR_HEI = 480
no_of_outputs = 16
player = None
AiPaddle = None
ball = None
FPS = 5000
size_of_paddle = 90
screen = None
size_of_spot = SCR_HEI / no_of_outputs
ROWS = 48
COLUMNS = 48
batch_size = 5
hit_count = 0

class AIPong():
        def __init__(self, player, AiPaddle, ball):
                clock = pygame.time.Clock()

                # Making the W&L text show up
                wlu_text = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
                wlu_blit = wlu_text.render("W&L", 1, (0, 0, 204))
                while True:
                        #process
                        for event in pygame.event.get():
                                        # MUST X OUT OF GAME AND HIT "CANCEL" ON POP-UP TO ENTER BELOW IF
                                        if event.type == pygame.QUIT:
                                                print("Game exited by user")
                                                exit()
                        ##process
                        #logic
                        ball.movement()
                        player.movement()
                        AiPaddle.movement()
                        ##logic
                        #draw
                        screen.fill((255, 255, 255))
                        ball.draw()
                        player.draw()
                        player.scoring()
                        AiPaddle.draw()
                        AiPaddle.scoring()
                        ball.update_count()
                        screen.blit(wlu_blit, (SCR_WID//2 - 60, 16))
                        ##draw
                        #_______
                        pygame.display.flip()
                        clock.tick(FPS)


class AiPaddle():
        def __init__(self, network):
                self.x, self.y = 16, SCR_HEI/2
                self.goal_y = self.y
                self.speed = 3
                self.padWid, self.padHei = 8, 85
                self.score = 0
                self.scoreFont = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
                self.network = network
       
        def scoring(self):
                scoreBlit = self.scoreFont.render(str(self.score), 1, (0, 0, 204))
                screen.blit(scoreBlit, (32, 16))
                if self.score == 10:
                        print("player 1 wins!")
                        exit()
       
        def movement(self):
                global have_new_input
                global testing_input
                # We will only move this paddle if new input has been given
                if have_new_input:
                        output = self.network.test(testing_input, batch_size) 
                        self.goal_y = convert_correct_form_to_location(output, size_of_spot)
                        # Reset the input flag to False
                        have_new_input = False
                check_sum = self.y - self.goal_y
                # check to see if the paddle is where it is supposed to be
                if check_sum != 0:
                        if check_sum < 0:
                                self.y += self.speed
                        else:
                                self.y -= self.speed
       
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, self.padWid, self.padHei))
 
class Player():
        def __init__(self):
                global size_of_spot
                self.x, self.y = SCR_WID-16, 0
                self.speed = 3
                self.padWid, self.padHei = 8, 1000
                self.score = 0
                self.scoreFont = pygame.font.Font("imagine_font/imagine_font.ttf", 64)

                
       
        def scoring(self):
                scoreBlit = self.scoreFont.render(str(self.score), 1, (0, 0, 204))
                screen.blit(scoreBlit, (SCR_WID-60, 16))
                if self.score == 10:
                        print("Player 2 wins!")
                        exit()
       
        def movement(self):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                        self.y -= self.speed
                elif keys[pygame.K_DOWN]:
                        self.y += self.speed
       
                if self.y <= 0:
                        self.y = 0
                elif self.y >= SCR_HEI-64:
                        self.y = SCR_HEI-64
       
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, self.padWid, self.padHei))
 
class Ball():
        def __init__(self):
                self.x, self.y = SCR_WID/2, SCR_HEI/2
                self.pic = np.zeros((ROWS, COLUMNS))
                # The last index below represents the previous y position
                # The first index below represents the eighth previous y picture
                self.pic_list = [np.zeros((ROWS, COLUMNS)) for i in range(8)]
                self.speed_x = -3
                self.speed_y = 3
                self.size = 8
                
        def movement(self):
                global have_new_input
                global testing_input       
                global hit_count
                self.x += self.speed_x
                self.y += self.speed_y

                if self.x < (SCR_WID//2) - 20:
                        # Update previous y values before changing self.y
                        for i in range(len(self.pic_list)-1):
                                self.pic_list[i] = self.pic_list[i+1]
                        self.pic_list[len(self.pic_list)-1] = self.pic
                        self.pic = np.zeros((ROWS, COLUMNS))
                        self.pic[int(self.y//10)][int(self.x//10)] = 1.0
                #wall col
                if self.y <= 0:
                        self.speed_y *= -1
                elif self.y >= SCR_HEI-self.size:
                        self.speed_y *= -1
 
                if self.x <= 0:
                        self.__init__()
                        player.score += 1
                        # We move the AI paddle back to a spot so it can hit the ball
                        AiPaddle.y = convert_correct_form_to_location(12, size_of_spot)
                        AiPaddle.goal_y = AiPaddle.y
                elif self.x >= SCR_WID-self.size:
                        self.__init__()
                        self.speed_x = 3
                        AiPaddle.score += 1
                ##wall col
                #paddle col
                #player

                for n in range(-self.size, AiPaddle.padHei):
                        if self.y == AiPaddle.y + n:
                                if self.x <= AiPaddle.x + AiPaddle.padWid:
                                        # Change the ball's direction if it hits player paddle
                                        self.speed_x *= -1
                                        hit_count += 1
                                        self.update_count()
                                        break
                        n += 1
                        
                #Player paddle
                for n in range(-self.size, player.padHei):
                        if self.y == player.y + n:
                                if self.x >= player.x - player.padWid:
                                        # Change the ball's direction if it hits AiPaddle paddle
                                        self.speed_x *= -1
                                        break
                        n += 1
                ##paddle col

                # We only want to see new input if the ball is in the left (seeing 8 pixels) half moving left
                if self.x == (SCR_WID//4) and self.speed_x < 0 and not have_new_input:
                        # We want to signify that we have received new input
                        # so that our AI Paddle knows to test this input
                        sum_list = np.zeros((ROWS, COLUMNS))
                        for lyst in self.pic_list:
                                sum_list += lyst
                        sum_list += self.pic
                        sl = sum_list.flatten()
                        have_new_input = True
                        testing_input = sl
                        #dumpimage(sl, ROWS, COLUMNS)

 
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, 8, 8))

        def update_count(self):

                global hit_count

                global screen

                score_text = pygame.font.Font("imagine_font/imagine_font.ttf", 64)

                score_blit = score_text.render(str(hit_count), 1, (0, 0, 204))

                screen.blit(score_blit, (SCR_WID//2 - 60, SCR_HEI - 60))





"""
convert_correct_form_to_location takes a spot number representing which spot
the paddle should be in and converts it to a corresponding location
"""
def convert_correct_form_to_location(spot_num, size_of_spot):
        return_val = spot_num*size_of_spot + (size_of_spot*.5) - (size_of_paddle/2)
        if return_val < 0:
                return 0
        if return_val > SCR_HEI - size_of_paddle:
                return SCR_HEI - size_of_paddle
        return return_val
        
def main():
        #Attack of the globals
        global SCR_WID
        global SCR_HEI
        global no_of_outputs
        global AiPaddle
        global player
        global ball
        global FPS
        global size_of_paddle
        global screen
        global size_of_spot
        
        screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
        pygame.display.set_caption("AI Pong")
        pygame.font.init()

        network = load("./data/best_lenet5_model.pkl")

        ball = Ball()
        player = Player()
        AiPaddle = AiPaddle(network)
        
        AIPong(player, AiPaddle, ball)

if __name__ == "__main__":
        main()

