import pygame
import time

pygame.init()

#create the board
screen = pygame.display.set_mode((800,800))

#Set up colours
WHITE = (255, 255, 255)
BLACK = (0,0,0)

#caption
pygame.display.set_caption("Chess")

x = 0
y = 0

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit =  True
        else:
            print("Game is playing")


pygame.quit()