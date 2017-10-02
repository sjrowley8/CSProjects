"""
Ryan Grant, Michael Holt, Mitch Olson, Stephen Rowley
CSCI 315
Final Project
pong_pixel.py
This file is used to gather training data by allowing humans to control
both pong paddles.
"""

import pygame
import pickle
from dumpimage import dumpimage
import numpy as np

global_training_input = []
global_training_output = []

SCR_WID, SCR_HEI = 960, 480
FPS = 20000 #MikeWasRight
player = None
ball = None
enemy = None
screen = None
ROWS = 48
COLUMNS = 48

class Pong():
        def __init__(self, player, enemy, ball):
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
                                                save_data("./data/batch1.pkl")
                                                exit()
                        ##process
                        #logic
                        ball.movement()
                        player.movement()
                        enemy.movement()
                        ##logic
                        #draw
                        screen.fill((255, 255, 255))
                        ball.draw()
                        player.draw()
                        player.scoring()
                        enemy.draw()
                        enemy.scoring()
                        screen.blit(wlu_blit, (SCR_WID//3 + 40, 16))
                        ##draw
                        #_______
                        pygame.display.flip()
                        clock.tick(FPS)


        
class Player():
        def __init__(self):
                self.x, self.y = 2, 0
                self.speed = 3
                self.padWid, self.padHei = 8, 1000
                self.score = 0
                self.scoreFont = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
       
        def scoring(self):
                scoreBlit = self.scoreFont.render(str(self.score), 1, (0, 0, 204))
                screen.blit(scoreBlit, (32, 16))
                if self.score == 10:
                        print("player 1 wins!")
                        exit()
       
        def movement(self):
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                        self.y -= self.speed
                elif keys[pygame.K_s]:
                        self.y += self.speed
       
                if self.y <= 0:
                        self.y = 0
                elif self.y >= SCR_HEI-64:
                        self.y = SCR_HEI-64
       
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, self.padWid, self.padHei))
 
class Enemy():
        def __init__(self):
                self.x, self.y = SCR_WID-10, 0
                self.speed = 3
                self.padWid, self.padHei = 8, 1000
                self.score = 0
                self.scoreFont = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
       
        def scoring(self):
                scoreBlit = self.scoreFont.render(str(self.score), 1, (0, 0, 204))
                screen.blit(scoreBlit, (SCR_HEI+92, 16))
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
                #self.pic = [0]*((ROWS)*(COLUMNS))
                self.pic = np.zeros((ROWS, COLUMNS))
                # The last index below represents the previous y position
                # The first index below represents the eighth previous y picture
                self.pic_list = [np.zeros((ROWS, COLUMNS)) for i in range(8)]
                self.speed_x = -3
                self.speed_y = 3
                self.size = 8
                
        def movement(self):
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
                        enemy.score += 1
                elif self.x >= SCR_WID-self.size:
                        self.__init__()
                        self.speed_x = 3
                        player.score += 1
                ##wall col
                #paddle col
                #player
                for n in range(-self.size, player.padHei):
                        if self.y == player.y + n:
                                if self.x <= player.x + player.padWid:
                                        # Change the ball's direction if it hits player paddle
                                        self.speed_x *= -1

                                        # TRAINING OUTPUT
                                        global global_training_output
                                        global_training_output.append(convert_location_to_correct_form(self.y))
                                        break
                        n += 1
                
                #enemy
                for n in range(-self.size, enemy.padHei):
                        if self.y == enemy.y + n:
                                if self.x >= enemy.x - enemy.padWid:
                                        # Change the ball's direction if it hits enemy paddle
                                        self.speed_x *= -1
                                        break
                        n += 1
                ##paddle col

                # We only want to see new input if the ball is in the left (seeing 8 pixels) half moving left
                if self.x == (SCR_WID//4) and self.speed_x < 0:
                        # Also save the player's and ball's y position (TRAINING INPUT)
                        global global_training_input
                        sum_list = np.zeros((ROWS, COLUMNS))
                        for lyst in self.pic_list:
                                sum_list += lyst
                        sum_list += self.pic
                        
                        global_training_input.append(sum_list.flatten())
                        #dumpimage(sum_list.flatten(), ROWS, COLUMNS)
                        
                        self.pic = np.zeros((ROWS, COLUMNS))
                        self.pic_list = [np.zeros((ROWS, COLUMNS)) for i in range(8)]

 
        def draw(self):
                pygame.draw.rect(screen, (0, 0, 204), (self.x, self.y, 8, 8))


"""
convert_location_to_correct_form takes a y position of a paddle and converts it
into its corresponding output within the network
"""
def convert_location_to_correct_form(y_location):
        spot_num = -1
        counter = 0
        current_location = 0
        no_of_outputs = 16
        size_of_spot = SCR_HEI / no_of_outputs
        while current_location < SCR_HEI and spot_num == -1:
                if y_location <= current_location + size_of_spot-1:
                        spot_num = counter
                counter += 1
                current_location += size_of_spot
        if current_location > SCR_HEI:
                spot_num = no_of_outputs-1    # We are at the last (lowest) spot in this case
        #return [0]*spot_num + [1] + [0]*((no_of_outputs-1)-spot_num)
        return spot_num

def save_data(fileName):
        global global_training_output
        global global_training_input
        with open(fileName, 'wb') as f:
                pickle.dump((global_training_input, global_training_output), f)
 
def load_data(fileName):
        with open(fileName, 'rb') as f:
                inputs, outputs = pickle.load(f)
        return (inputs, outputs)

def main():
        global SCR_WID, SCR_HEI, FPS, ball, player, enemy, screen

        screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
        pygame.display.set_caption("Pong")
        pygame.font.init()
        clock = pygame.time.Clock()
         
        ball = Ball()
        player = Player()
        enemy = Enemy()
        # Making the W&L text show up
        wlu_text = pygame.font.Font("imagine_font/imagine_font.ttf", 64)
        wlu_blit = wlu_text.render("W&L", 1, (0, 0, 204))
        Pong(player, enemy, ball)

if __name__ == "__main__":
        main()
