import pygame
import time
from piece import *

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

def input_board(width=800, height=800):
    input_squares = {}
    the_height = 0
    for i in range(8):
        the_position = 0
        for j in range(8):
            input_squares[(i, j)] = {"input": pygame.Rect(the_position, the_height, 100, 100), "rect": (the_position, the_height, 100, 100)}
            the_position += 100
        the_height += 100
    return input_squares

def draw_piece(the_piece, place_dictionary=input_board):
    location = the_piece.getPosition()
    if location == (-1, -1):
        return (-100, -100)
    else:
        the_position = place_dictionary[location]["rect"]
        return(the_position[0] + 8.5, the_position[1] + 8.5)


#caption
pygame.display.set_caption("Chess")
input_board = input_board()
x = 0
y = 0

gameExit = False

while not gameExit:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        gameExit = True
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            for key in input_board:
                if input_board[key]["input"].collidepoint(event.pos):
                    print(f"{key} clicked")
                    if selected == key:
                        selected = (-1, -1)
                    else:
                        selected = key
            
    
    screen.fill(WHITE)

    the_positions = board_fill()
    for position in the_positions:
        screen.fill(BLACK, position)
    if selected != (-1, -1):
        screen.fill(GREEN, input_board[selected]["rect"])

    pygame.display.flip()


pygame.quit()
