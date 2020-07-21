class Piece():

    def __init__(self, x, y, side=0):
        self.x = x
        self.y = y
        self.side = side

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


class Pawn(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        self.start_x = x
        self.start_y = y
    
    def getAllowedMoves(self):
        if self.side == 0:
            mult = (-1, -2)
        else:
            mult = (1, 2)
        if self.x == self.start_x and self.y == self.start_y:
            return [(self.x, self.y+mult[0]), (self.x, self.y+mult[1])]
        else:
            return [(self.x, self.y+mult[0])]


class Rook(Piece):

    def getAllowedMoves(self):
        startRangeX = 0 - self.x
        endRangeX = 7 - self.x
        startRangeY = 0 - self.y
        endRangeY = 7 - self.y
        x_moves = [(self.x + i, self.y) for i in range(startRangeX, endRangeX + 1)]
        y_moves = [(self.x, self.y + i) for i in range(startRangeY, endRangeY + 1)]
        return x_moves + y_moves

class Bishop(Piece):

    def getAllowedMoves(self):
        moves = []
        for x in range(8):
            for y in range(8):
                if abs(self.x - x) == abs(self.y - y) and (self.x != x and self.y != y):
                    moves.append((x, y))
        return moves

class Queen(Piece):

    def diagonal(self):
        moves = []
        for x in range(8):
            for y in range(8):
                if abs(self.x - x) == abs(self.y - y) and (self.x != x and self.y != y):
                    moves.append((x, y))
        return moves
    
    def straight(self):
        startRangeX = 0 - self.x
        endRangeX = 7 - self.x
        startRangeY = 0 - self.y
        endRangeY = 7 - self.y
        x_moves = [(self.x + i, self.y) for i in range(startRangeX, endRangeX + 1)]
        y_moves = [(self.x, self.y + i) for i in range(startRangeY, endRangeY + 1)]
        return x_moves + y_moves

    def getAllowedMoves(self):
        return self.diagonal() + self.straight()

class King(Piece):

    def getAllowedMoves(self):
        moves = []
        #Consider straight line on x
        if self.x == 0:
            moves.append((self.x + 1, self.y))
        elif self.x == 7:
            moves.append((self.x - 1, self.y))
        else:
            moves += [(self.x + 1, self.y), (self.x - 1, self.y)]
        
        #Consider straight line on y
        if self.y == 0:
            moves.append((self.x, self.y + 1))
        elif self.y == 7:
            moves.append((self.x, self.y - 1))
        else:
            moves += [(self.x, self.y + 1), (self.x, self.y - 1)]

        #Consider Diagonal
        if self.x == 0:
            if self.y == 0:
                moves.append((self.x + 1, self.y + 1))
            elif self.y == 7:
                moves.append((self.x + 1, self.y - 1))
            else:
                moves += [(self.x + 1, self.y + 1), (self.x + 1, self.y - 1)]
        elif self.y == 0:
            if self.x == 7:
                moves.append((self.x - 1, self.y - 1))
            else:
                moves += [(self.x + 1, self.y + 1), (self.x - 1, self.y + 1)]
        else:
            moves += [(self.x + 1, self.y + 1),
                    (self.x + 1, self.y - 1),
                    (self.x - 1, self.y + 1),
                    (self.x - 1, self.y -1)]

        return moves

class Knight(Piece):

    def getAllowedMoves(self):
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
            if (new_move[0] >= 0 or new_move[0] <= 7) or (new_move[1] >= 0 or new_move[1] <= 7):
                moves.append(new_move)
        return moves
    






