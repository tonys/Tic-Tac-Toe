import sys

class Board(object):

	def __init__(self):
                self.data = {}
                self.players = [None, None]
                self.row_list = [
                        [(0,0),(0,1),(0,2)],
                        [(1,0),(1,1),(1,2)],
                        [(2,0),(2,1),(2,2)],
                        [(0,0),(1,0),(2,0)],
                        [(0,1),(1,1),(2,1)],
                        [(0,2),(1,2),(2,2)],
                        [(0,0),(1,1),(2,2)],
                        [(2,0),(1,1),(0,2)],
                ]
                self.reset_data()

        def reset_data(self):
                for a in range(3):
                        for d in range(3):
                                self.data[(a,d)] = None
                self.update_scorebds()

        def set_player1(self, player):
                self.players[0] = player

        def set_player2(self, player):
                self.players[1] = player

        def update(self, player, move):
                if not self.data[move]:
                        self.data[move] = player.letter
                else:
                        raise RuntimeError, 'That position already filled.'
                self.update_scorebds()

        def reset(self):
                self.reset_data()

        def display(self):
                pass

        def update_scorebds(self):
                for player in self.players:
                        if player:
                                player.update_scorebd(self.data)
        
        def check_win(self):
                possible = 0
                for row in self.row_list:
                        player1_score = 0
                        player2_score = 0
                        for loc in row:
                                if self.data[loc] == self.players[0].letter:
                                        player1_score += 1
                                elif self.data[loc] == self.players[1].letter:
                                        player2_score += 1
                                else:
                                        possible += 1
                        if player1_score == 3:
                                return self.players[0]
                        if player2_score == 3:
                                return self.players[1]
                if not possible:
                        return 'draw'
                return None

class Player(object):
        
        def __init__(self, name, letter, game_board):
                self.name = name
                self.letter = letter
                self.update_scorebd(game_board.data)

        def error(self, msg):
                pass

        def update_scorebd(self, game_board):
                pass

        def choose(self):
                return None

class Display(object):

        def __init__(self, board, player1, player2):
                self.board = board
                self.player1 = player1
                self.player2 = player2
                self.reset_choice = (-3,-3)
                self.quit_choice = (-2,-2)

        def init(self):
                pass

        def update():
                pass

        def new_game():
                pass

        def get_choice(self, player):
                while 1:
                        choice = player.choose()
                        if isinstance(choice, tuple):
                                return choice
                        elif isinstance(choice, str):
                                c = choice.strip()
                                if c == 'quit':
                                        return self.quit_choice
                                elif c == 'reset':
                                        return self.reset_choice
                                elif c[0] == '(' and c[-1] == ')':
                                        return eval(choice)
        
        def reset_game(self):
                self.board.reset()
                self.active_player = self.player1
                self.new_game()
                self.update()

        def toggle_active_player(self):
                if self.active_player == self.player1:
                        self.active_player = self.player2
                else:
                        self.active_player = self.player1
        
        def mainloop(self):
                winner = None
                self.active_player = self.player1
                self.update()
                while 1:
                        choice = self.get_choice(self.active_player)
                        if choice == self.reset_choice:
                                self.reset_game()
                                continue
                        elif choice == self.quit_choice:
                                sys.exit(0)
                        try:
                                self.board.update(self.active_player, choice)
                        except RuntimeError, msg:
                                self.active_player.error(msg)
                                continue
                        self.update()
                        winner = self.board.check_win()
                        if winner:
                                self.update(winning_player=winner)
                                self.reset_game()
                                continue
                        self.toggle_active_player()
