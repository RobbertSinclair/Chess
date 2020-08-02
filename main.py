import pygame
import time
from piece import *

pygame.init()

#create the window
screen = pygame.display.set_mode((800,800))

#Set up colours
WHITE = (255, 255, 255)
BLACK = (40,40,40)
GREEN = (0,128,0)
ORANGE = (255, 69, 0)

board = [[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]



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

def input_board(pieces, width=800, height=800):
    input_squares = {}
    the_height = 0
    input_squares["check"] = False
    input_squares["check_attacker"] = 0
    input_squares["check_moves"] = []
    piece_locations = {piece.getPosition(): piece for piece in pieces}
    for i in range(8):
        the_position = 0
        for j in range(8):
            if (j,i) in piece_locations.keys():
                the_piece = piece_locations[(j,i)]
            else:
                the_piece = 0 
            input_squares[(j, i)] = {"input": pygame.Rect(the_position, the_height, 100, 100), 
                                    "rect": (the_position, the_height, 100, 100),
                                    "piece": the_piece}
            the_position += 100
        the_height += 100
    return input_squares

def set_up_board():
    #Place Pawns
    pieces = []
    for i in range(8):
        pieces.append(Pawn(i,1,side=1))
        pieces.append(Pawn(i,6))
    #Place Rooks
    pieces.append(Rook(0,0,1))
    pieces.append(Rook(7,0,1))
    pieces.append(Rook(0,7))
    pieces.append(Rook(7,7))
    #Place Knights
    pieces.append(Knight(1,0,1))
    pieces.append(Knight(6,0,1))
    pieces.append(Knight(1,7))
    pieces.append(Knight(6,7))
    #Place Bishops
    pieces.append(Bishop(2,0,1))
    pieces.append(Bishop(5,0,1))
    pieces.append(Bishop(2,7))
    pieces.append(Bishop(5,7))
    #Place Kings
    pieces.append(King(4,0,1))
    pieces.append(King(4,7))
    #Place Queen
    pieces.append(Queen(3,0,1))
    pieces.append(Queen(3,7))
    return pieces

pieces = set_up_board()
input_board = input_board(pieces)
side_pieces = {0: [piece for piece in pieces if piece.getSide() == 0],
               1: [piece for piece in pieces if piece.getSide() == 1],
               "white_king": [piece for piece in pieces if str(piece) == "K" and piece.getSide() == 0][0],
               "black_king": [piece for piece in pieces if str(piece) == "K" and piece.getSide() == 1][0]
               }

def draw_piece(the_piece, place_dictionary=input_board):
    location = the_piece.getPosition()
    if location == (-1, -1):
        return (-100, -100)
    else:
        the_position = place_dictionary[location]["rect"]
        return(the_position[0] + 8, the_position[1] + 8)

#caption
pygame.display.set_caption("Chess")

x = 0
y = 0
side_turn = 0
gameExit = False
selected = (-1, -1)

while not gameExit:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        gameExit = True
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            for key in input_board:
                if key != "check" and key != "check_moves" and key != "check_attacker":
                    if input_board[key]["input"].collidepoint(event.pos):
                        the_piece = 0
                        print(f"{key} clicked")
                        if selected == [key]:
                            selected = (-1, -1)
                        elif key in selected:
                            piece_location = input_board[the_position]["piece"].getPosition()
                            #Taking manouver
                            print("The value of the piece at {0} is {1}".format(key, input_board[key]["piece"]))
                            if input_board[key]["piece"] != 0:
                                print("This has run")
                                if input_board[key]["piece"].getSide() != input_board[the_position]["piece"].getSide():
                                    taken_piece_index = pieces.index(input_board[key]["piece"])
                                    input_board[key]["piece"].setPosition(-1, -1)
                                    pieces[taken_piece_index].setPosition(-1,-1)
                                    print(f"The position of the taken piece is {pieces[taken_piece_index].getPosition()}")
                                    print(f"The result of draw_piece({pieces[taken_piece_index]}) is {draw_piece(pieces[taken_piece_index])}")

                                    #the_pieces.pop(taken_piece_index)
                            #Move the piece
                            piece_index = pieces.index(input_board[the_position]["piece"])
                            input_board[the_position]["piece"] = 0
                            pieces[piece_index].setPosition(key[0], key[1])
                            the_king = pieces[piece_index].getEnemyKing(side_pieces)
                            input_board[key]["piece"] = pieces[piece_index]
                            selected = (-1, -1)
                            if str(input_board[key]["piece"]) == "K":
                                the_moves = input_board[key]["piece"].getAllowedMoves(input_board, side_pieces, side_turn)
                            else:
                                the_moves = input_board[key]["piece"].getAllowedMoves(input_board, side_pieces)
                            kingPos = the_king.getPosition()
                            if kingPos in the_moves:
                                input_board["check_attacker"] = input_board[key]["piece"]
                                print("The attacking piece is {0}".format(input_board["check_attacker"]))
                                if str(input_board["check_attacker"]) == "Q" or str(input_board["check_attacker"]) == "R" or input_board["check_attacker"] == "B":
                                    input_board["check_moves"] = input_board["check_attacker"].getDangerMoves(kingPos) + [input_board["check_attacker"].getPosition()]
                                elif str(input_board["check_attacker"]) == "N" or str(input_board["check_attacker"]) == "P":
                                    input_board["check_moves"] = [input_board["check_attacker"].getPosition()]

                                else:
                                    input_board["check_moves"] = input_board["check_attacker"].getAllowedMoves(input_board, side_pieces)
                                print(input_board["check_moves"])
                                input_board["check"] = True
                            else:
                                input_board["check_attacker"] = 0
                                input_board["check_moves"] = []
                                input_board["check"] = False
                            #Change the side turn
                            if key != piece_location:
                                if side_turn == 0:
                                    side_turn = 1
                                else:
                                    side_turn = 0
                        else:
                            the_piece = input_board[key]["piece"]
                            selected = [key]
                            
                            if the_piece != 0 and the_piece.getSide() == side_turn:
                                the_position = the_piece.getPosition()
                                if str(the_piece) != "K":
                                    selected = selected + the_piece.getAllowedMoves(input_board, side_pieces)
                                else:
                                    selected = selected + the_piece.getAllowedMoves(input_board, side_pieces, side_turn)
    

    screen.fill(WHITE)

    the_positions = board_fill()
    for position in the_positions:
        screen.fill(BLACK, position)
    if selected != (-1, -1):
        for select in selected:
            screen.fill(GREEN, input_board[select]["rect"])

    if input_board["check"]:
        screen.fill(ORANGE, input_board[the_king.getPosition()]["rect"])


    for piece in pieces:
        the_image = pygame.image.load(piece.get_icon())
        if draw_piece(piece) != (-100, -100):
            screen.blit(the_image, draw_piece(piece))

    pygame.display.flip()


pygame.quit()
