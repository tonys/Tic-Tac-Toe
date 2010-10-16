import ttt_internals, sys

class Display(ttt_internals.Display):

        def update(self, winning_player=None):
                if winning_player:
                        if winning_player == 'draw':
                                print "\n\nThe game results in a DRAW\n"
                        else:
                                print "\n\n%s's have WON the game !!!\n" % (winning_player.letter)
                                print "   CONGRATULATIONS\n\n\n"
                        return
                for row in self.board.row_list[:3]:
                        out = ['.', '.', '.']
                        for i in range(3):
                                if self.board.data[row[i]]:
                                        out[i] = self.board.data[row[i]]
                        print '          %s %s %s\n' % ( out[0], out[1], out[2] )
                print '\n\n'

        def new_game(self):
                print '\n\nStarting a NEW GAME !!!\n'
                print '     GOOD LUCK\n\n'
