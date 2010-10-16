import ttt_internals, time, math

class Player(ttt_internals.Player):

        def __init__(self, name, letter, game_board):
                self.name = name
                self.scorebd = {}
                self.row_list = game_board.row_list
                ttt_internals.Player.__init__(self, name, letter, game_board)

        def score_loc(self, loc, game_data):

                """ This routine expects that the calling routine has already
                checked for collision.  """

                score = 0
                loc_score = 0
                for row in self.row_list:
                        if loc in row:
                                p1_score = 0
                                p2_score = 0
                                for nloc in row:
                                        if game_data[nloc] == self.letter:
                                                p1_score += 1
                                        elif game_data[nloc] is not None:
                                                p2_score += 1
                                if p1_score and p2_score: # both already blocked - no val this row
                                        continue
                                elif p2_score == 0: # no opposition
                                        loc_score += 1*math.pow(10,p1_score)
                                else: # opposition
                                        loc_score += 5*math.pow(10,(p2_score - 1))
                return loc_score

        def update_scorebd(self, game_board):

                """ This will attempt to score the positions on the board.
                Each necessary position is evaluated against the rows it is
                contained by.  If the position is already filled, it is set to
                -1.  If the opposition has any pieces in the row, the value of
                the position for that row is 5*10^(n-1) where n = the number of
                pieces the opposition has in the row..  If the opposition has
                no pices in the row, the value of the position for that row is
                1*10^n where n is the number of pieces the player has in the
                row.  The final score for the position is the sum of the score
                for each row containing it. """

                for loc in game_board.iterkeys():
                        if game_board[loc] is not None:
                                self.scorebd[loc] = -1
                                continue
                        self.scorebd[loc] = self.score_loc(loc, game_board)

        def best_move(self):

                """ This will attempt to return the best move for the given
                player. """

                spec_excp1 = {(0, 1): 15.0, (1, 2): 15.0, (0, 0): 20.0,
                              (2, 1): 15.0, (0, 2): -1, (2, 0): -1,
                              (2, 2): 20.0, (1, 0): 15.0, (1, 1): -1}
                spec_excp2 = {(0, 1): 15.0, (1, 2): 15.0, (0, 0): -1,
                              (2, 1): 15.0, (0, 2): 20.0, (2, 0): 20.0,
                              (2, 2): -1, (1, 0): 15.0, (1, 1): -1}
                if self.scorebd == spec_excp1 or self.scorebd == spec_excp2:
                        return (0,1)
                max_score = 0
                max_loc = None
                for loc, score in self.scorebd.iteritems():
                        if score > max_score:
                                max_score = score
                                max_loc = loc
                if not max_loc:
                        return 'reset'
                return max_loc

        def choose(self):

                """ This simply performs sleep(2) (to simulate cognition) and
                returns the result of the best_move() calculation.  """

                time.sleep(2)
                return self.best_move()
