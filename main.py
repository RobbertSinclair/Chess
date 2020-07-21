import pygame
import time

pygame.init()

#create the board
screen = pygame.display.set_mode((800,800))

#Set up colours
WHITE = (255, 255, 255)
BLACK = (0,0,0)

#Define the areas to fill the board
def board_fill(width = 800, height = 800):
    positions = []
    zero_start = True
    the_height = 0
    while the_height < height:
        i = 0
        if zero_start:
            the_start = 0
        else:
            the_start = 100
        while i < width:
            new_tuple = (the_start + i, the_height, 100, 100)
            positions.append(new_tuple)
            i += 200
        the_height += 100
        zero_start = not zero_start
    return positions

#caption
pygame.display.set_caption("Chess")

x = 0
y = 0

gameExit = False

while not gameExit:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        gameExit = True
    
    screen.fill(WHITE)

    the_positions = board_fill()
    for position in the_positions:
        screen.fill(BLACK, position)


    pygame.display.flip()


pygame.quit()
