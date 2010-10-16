import ttt_internals, sys

class Player(ttt_internals.Player):

        def error(self, msg):
                print str(msg) + '\n'

        def choose(self):
                print '%s:' % self.name
                choice = sys.stdin.readline()
                return choice
