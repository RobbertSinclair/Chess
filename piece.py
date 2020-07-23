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

    def get_position(self):
        return(self.x, self.y)
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
    def get_icon(self):
        return self.icon
    
    def getSide(self):
        return self.side

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
    
    def getAllowedMoves(self, input_board):
        if self.side == 0:
            mult = (-1, -2)
        else:
            mult = (1, 2)
        if self.x == self.start_x and self.y == self.start_y:
            return [(self.x, self.y+mult[0]), (self.x, self.y+mult[1])]
        else:
            return [(self.x, self.y+mult[0])]


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
        startRangeX = 0 - self.x
        endRangeX = 7 - self.x
        startRangeY = 0 - self.y
        endRangeY = 7 - self.y
        x_moves = [(self.x + i, self.y) for i in range(startRangeX, endRangeX + 1)]
        y_moves = [(self.x, self.y + i) for i in range(startRangeY, endRangeY + 1)]
        return x_moves + y_moves

class Bishop(Piece):
    
    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_bishop.png"
        else:
            self.icon = "black_bishop.png"
    
    def __str__(self):
        return "B"

    def getAllowedMoves(self):
        moves = []
        for x in range(8):
            for y in range(8):
                if abs(self.x - x) == abs(self.y - y) and (self.x != x and self.y != y):
                    moves.append((x, y))
        return moves

class Queen(Piece):
    
    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_queen.png"
        else:
            self.icon = "black_queen.png"
    
    def __str__(self):
        return "Q"
   
    def diagonal(self, input_board):
        moves = []
        for x in range(8):
            for y in range(8):
                if abs(self.x - x) == abs(self.y - y) and (self.x != x and self.y != y):
                    moves.append((x, y))
        return moves
    
    def straight(self, input_board):
        startRangeX = 0 - self.x
        endRangeX = 7 - self.x
        startRangeY = 0 - self.y
        endRangeY = 7 - self.y
        x_moves = [(self.x + i, self.y) for i in range(startRangeX, endRangeX + 1)]
        y_moves = [(self.x, self.y + i) for i in range(startRangeY, endRangeY + 1)]
        return x_moves + y_moves

    def getAllowedMoves(self, input_board):
        return self.diagonal() + self.straight()

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
            if (new_move[0] >= 0 and new_move[1] <= 7) and (new_move[1] >= 0 and new_move[1] <= 7):
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
            if (new_move[0] >= 0 and new_move[0] <= 7) and (new_move[1] >= 0 and new_move[1] <= 7):
                moves.append(new_move)
        return moves
    






