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

                
            
