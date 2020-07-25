class Piece():

    def __init__(self, x, y, side=0):
        self.x = x
        self.y = y
        if side == 0:
            self.side = 0
        else:
            self.side = 1

    def move(self, move_tuple):
        allowed = self.getAllowedMoves()
        if(move_tuple in allowed):
            self.x = move_tuple[0]
            self.y = move_tuple[1]
        else:
            print("INVALID MOVE")

    def set_taken(self):
        self.x = -1
        self.y = -1

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getPosition(self):
        return(self.x, self.y)

    def get_icon(self):
        return self.icon

    def getSide(self):
        return self.side
    
    def checkAllyOccupied(self, position, input_board):
        piece = input_board[position]["piece"]
        if piece == 0 or piece.getSide() != self.getSide():
            return False
        else:
            return True
    
    def removeElts(self, original, remove):
        for rem in remove:
            if rem in original:
                og_index = original.index(rem)
                original.pop(og_index)
        return original

    def removePlaces(self, coord):
        moves = []
        position = self.getPosition()
        move_diff = [coord[0] - position[0], coord[1] - position[1]]
        print(f"Move diff before: {move_diff}")
        for i in range(len(move_diff)):
            if move_diff[i] != 0:
                move_diff[i] = move_diff[i] // abs(move_diff[i])
        print(f"Move diff after: {move_diff}")
        mult = 0
        new_move = (0,0)
        while (new_move[0] >= 0 and new_move[0] <= 7) and (new_move[1] >= 0 and new_move[1] <= 7):
            new_move = (coord[0] + (mult * move_diff[0]), coord[1] + (mult * move_diff[1]))
            if (new_move[0] >= 0 and new_move[0] <= 7) and (new_move[1] >= 0 and new_move[1] <= 7):
                moves.append(new_move)
            mult += 1
        return moves

    def straight(self, input_board):
        startRangeX = 0 - self.x
        endRangeX = 7 - self.x
        startRangeY = 0 - self.y
        endRangeY = 7 - self.y
        remove = []
        x_moves = [(self.x + i, self.y) for i in range(startRangeX, endRangeX + 1)]
        current = x_moves.index((self.x, self.y))
        x_moves.pop(current)
        y_moves = [(self.x, self.y + i) for i in range(startRangeY, endRangeY + 1)]
        current = y_moves.index((self.x, self.y))
        y_moves.pop(current)
        the_moves = x_moves + y_moves
        for coord in the_moves:
            print("Loop")
            if input_board[coord]["piece"] != 0:
                remove = remove + self.removePlaces(coord)
                print(remove)
                if not self.checkAllyOccupied(coord, input_board):
                    index = remove.index(coord)
                    remove.pop(index)    
        the_moves = self.removeElts(the_moves, remove)
        print(f"The possible moves are {the_moves}")
        return the_moves

    def diagonal(self, input_board):
        moves = []
        remove = []
        for x in range(8):
            for y in range(8):
                if abs(self.x - x) == abs(self.y - y) and (self.x != x and self.y != y):
                    moves.append((x, y))
                    if input_board[(x,y)]["piece"] != 0:
                        remove = remove + self.removePlaces((x,y))
                        if not self.checkAllyOccupied((x,y), input_board):
                            index = remove.index((x,y))
                            remove.pop(index)
        moves = self.removeElts(moves, remove)
        return moves
        
class Pawn(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        self.start_x = x
        self.start_y = y
        if self.side == 0:
            self.icon = "white_pawn.png"
        else:
            self.icon = "black_pawn.png"

    def __str__(self):
        return "P"

    def checkOccupied(self, position, input_board):
        piece = input_board[position]["piece"]
        if piece == 0:
            return False
        else:
            return True

    def checkTake(self, input_board):
        possible_takes = []
        if self.getSide() != 0:
            diagonal = [(1, 1), (-1, 1)]
        else:
            diagonal = [(1, -1), (-1, -1)]
        pot_positions = []
        for di in diagonal:
            if (self.x + di[0] >= 0 and self.x + di[0] <= 7) and (self.y + di[1] >= 0 and self.y + di[1] <= 7):
                position = (self.x + di[0], self.y + di[1])
                pot_positions.append(position)
        print(f"The potential diagonal positions are {pot_positions}")
        for pos in pot_positions:
            if input_board[pos]["piece"] != 0 and input_board[pos]["piece"].getSide() != self.side:
                possible_takes.append(pos)
        return possible_takes

    def getAllowedMoves(self, input_board):
        moves = []
        if self.side == 0:
            mult = (-1, -2)
        else:
            mult = (1, 2)
        print(self.checkTake(input_board))
        if self.y + mult[0] >= 0 and self.y + mult[1] <= 7:
            if self.x == self.start_x and self.y == self.start_y:
                pot_moves = [(self.x, self.y+mult[0]), (self.x, self.y+mult[1])]
            else:
                pot_moves = [(self.x, self.y+mult[0])]
            print(f"The potential main moves are {pot_moves}")
        else:
            return []
        for move in pot_moves:
            if not self.checkOccupied(move, input_board):
                moves.append(move)
        return moves + self.checkTake(input_board)

class Rook(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_rook.png"
        else:
            self.icon = "black_rook.png"

    def __str__(self):
        return "R"

    def getAllowedMoves(self, input_board):
        return self.straight(input_board)

class Bishop(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_bishop.png"
        else:
            self.icon = "black_bishop.png"

    def __str__(self):
        return "B"

    def getAllowedMoves(self, input_board):
        return self.diagonal(input_board)

class Queen(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_queen.png"
        else:
            self.icon = "black_queen.png"

    def __str__(self):
        return "Q"

    def getAllowedMoves(self, input_board):
        return self.diagonal(input_board) + self.straight(input_board)

class King(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_king.png"
        else:
            self.icon = "black_king.png"

    def __str__(self):
        return "K"

    def getAllowedMoves(self, input_board):
        moves = []
        #Consider all of the possible moves
        differences = [(1,0),
                       (0,1),
                       (1,1),
                       (-1,0),
                       (0,-1),
                       (1,-1),
                       (-1,1),
                       (-1,-1)]
        
        for diff in differences:
            new_move = (self.x + diff[0], self.y + diff[1])
            if (new_move[0] >= 0 and new_move[1] <= 7) and (new_move[1] >= 0 and new_move[1] <= 7) and not self.checkAllyOccupied(new_move, input_board):
                moves.append(new_move)
        return moves
        
class Knight(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_knight.png"
        else:
            self.icon = "black_knight.png"

    def __str__(self):
        return "N"

    def getAllowedMoves(self, input_board):
        moves = []
        difference = [(2,1),
                      (2,-1),
                      (-2,1),
                      (-2,-1),
                      (1,2),
                      (1,-2),
                      (-1,2),
                      (-1,-2)]
        for diff in difference:
            new_move = (self.x + diff[0], self.y + diff[1])
            if (new_move[0] >= 0 and new_move[0] <= 7) and (new_move[1] >= 0 and new_move[1] <= 7) and not self.checkAllyOccupied(new_move, input_board):
                moves.append(new_move)
        return moves
