class Piece():

    def __init__(self, x, y, side=0):
        self.x = x
        self.y = y
        if side == 0:
            self.side = 0
        else:
            self.side = 1

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getPosition(self):
        return (self.x, self.y)

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

    def determineKing(self, side_pieces):
        if self.getSide() == 0:
            return side_pieces["white_king"]
        else:
            return side_pieces["black_king"]

    def getEnemyKing(self, side_pieces):
        if self.getSide() == 0:
            return side_pieces["black_king"]
        else:
            return side_pieces["white_king"]

    def defend(self, playerMoves, attackMoves):
        defence = []
        for move in playerMoves:
            if move in attackMoves:
                defence.append(move)
        return defence

    def checkOccupied(self, position, input_board):
        piece = input_board[position]["piece"]
        if piece == 0:
            return False
        else:
            return True

    def getDangerMoves(self, coord):
        moves = []
        position = self.getPosition()
        move_diff = [coord[0] - position[0], coord[1] - position[1]]
        for i in range(len(move_diff)):
            if move_diff[i] != 0:
                move_diff[i] = move_diff[i] // abs(move_diff[i])
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
            if input_board[coord]["piece"] != 0:
                remove = remove + self.getDangerMoves(coord)
                if not self.checkAllyOccupied(coord, input_board):
                    index = remove.index(coord)
                    remove.pop(index)    
        the_moves = self.removeElts(the_moves, remove)
        return the_moves

    def diagonal(self, input_board):
        moves = []
        remove = []
        for x in range(8):
            for y in range(8):
                if abs(self.x - x) == abs(self.y - y) and (self.x != x and self.y != y):
                    moves.append((x, y))
                    if input_board[(x,y)]["piece"] != 0:
                        remove = remove + self.getDangerMoves((x,y))
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
        for pos in pot_positions:
            if input_board[pos]["piece"] != 0 and input_board[pos]["piece"].getSide() != self.side:
                possible_takes.append(pos)
        return possible_takes


    def removePlaces(self, moves, input_board):
        remove = []
        for move in moves:
            if move not in input_board["check_moves"]:
                remove.append(move)
        for rem in remove:
            move_index = moves.index(rem)
            moves.pop(move_index)
        return moves
                
        


    def getAllowedMoves(self, input_board, side_pieces):
        moves = []
        if self.side == 0:
            mult = (-1, -2)
        else:
            mult = (1, 2)
        if self.y + mult[0] >= 0 and self.y + mult[1] <= 7 and self.y + mult[0] <= 7 and self.y + mult[1] >= 0:
            if self.x == self.start_x and self.y == self.start_y:
                pot_moves = [(self.x, self.y+mult[0]), (self.x, self.y+mult[1])]
            else:
                pot_moves = [(self.x, self.y+mult[0])]
        else:
            return []
        for move in pot_moves:
            if not self.checkOccupied(move, input_board):
                moves.append(move)
        moves = moves + self.checkTake(input_board)
        if input_board["check"]:
            moves = self.removePlaces(moves, input_board)
        return moves
            
        

class Rook(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_rook.png"
        else:
            self.icon = "black_rook.png"

    def __str__(self):
        return "R"

    def getAllowedMoves(self, input_board, side_pieces):
        moves = self.straight(input_board)
        if not input_board["check"]:
            return moves
        else:
            attacker = input_board["check_moves"]
            defense = self.defend(moves, attacker)
            return defense

class Bishop(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_bishop.png"
        else:
            self.icon = "black_bishop.png"

    def __str__(self):
        return "B"

    def getAllowedMoves(self, input_board, side_pieces):
        moves = self.diagonal(input_board)
        if not input_board["check"]:
            return moves
        else:
            attacker = input_board["check_moves"]
            defense = self.defend(moves, attacker)
            return defense
        
class Queen(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_queen.png"
        else:
            self.icon = "black_queen.png"

    def __str__(self):
        return "Q"

    def getAllowedMoves(self, input_board, side_pieces):
        moves = self.diagonal(input_board) + self.straight(input_board)
        if not input_board["check"]:    
            return moves
        else:
            attacker = input_board["check_moves"]
            defense = self.defend(moves, attacker)
            return defense

class King(Piece):

    def __init__(self, x, y, side=0):
        super().__init__(x, y, side)
        if self.side == 0:
            self.icon = "white_king.png"
        else:
            self.icon = "black_king.png"
    
    def __str__(self):
        return "K"
    
    def removeCheckAreas(self, input_board, side_pieces, moves, side_turn):
        remove = []
        if self.getSide() == 0:
            enemy_side = 1
        else:
            enemy_side = 0
        for piece in side_pieces[enemy_side]:
            if str(piece) == "P":
                remove = remove + piece.checkTake(input_board)
            else:
                if str(piece) != "K":
                    enemyMoves = piece.getAllowedMoves(input_board, side_pieces)
                else:
                    enemyMoves = piece.getAllowedMoves(input_board, side_pieces, side_turn)
                for move in enemyMoves:
                    if move in moves:
                        remove.append(move)
                for move in moves:
                    if move in input_board["check_moves"]:
                        remove.append(move)    
        return remove

    def getAttack(self, input_board, side_pieces):
        position = self.getPosition()
        if self.getSide() == 0:
            enemySide = 1
        else:
            enemySide = 0
        potential_attackers = side_pieces[enemySide]
        print(f"The potential attackers are {potential_attackers}")
        time.sleep(1)
        for piece in potential_attackers:
            if str(piece) != "K":
                print(f"Executing the getAllowedMoves method for {piece}")
                time.sleep(0.2)
                enemyMoves = piece.getAllowedMoves(input_board, side_pieces)
                if position in enemyMoves:
                    return enemyMoves + [piece.getPosition()]
        return []
                    

    def getAllowedMoves(self, input_board, side_pieces, side_turn):
        moves = []
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
        if len(moves) != 0 and side_turn == self.getSide():
            remove = self.removeCheckAreas(input_board, side_pieces, moves, side_turn)
            print(f"Remove is {remove}")
            moves = self.removeElts(moves, remove)
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

    def getAllowedMoves(self, input_board, side_pieces):
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
        if not input_board["check"]:    
            return moves
        else:
            attacker = input_board["check_moves"]
            defense = self.defend(moves, attacker)
            return defense
