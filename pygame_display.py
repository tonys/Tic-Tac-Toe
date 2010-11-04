import sys, pygame, ttt_internals, computer_player

class PG_Board(object):
        
        def __init__(self, pos_x=0, pos_y=0, board_image=None, x_image=None, o_image=None):
                self.pos_x = pos_x
                self.pos_y = pos_y
                self.board_loc = pos_x, pos_y
                self.board_image = board_image
                #self.board_d = pygame.image.load(board_image)
                self.x_image = x_image
                self.o_image = o_image
                self.x_piece = pygame.image.load(x_image)
                self.o_piece = pygame.image.load(o_image)
                self.blank = pygame.image.load("blank.png")
                self.board_locs = [[] for i in range(10)]
                self.board_locs[1] = 10, 10
                self.board_locs[2] = 165, 10
                self.board_locs[3] = 320, 10
                self.board_locs[4] = 10, 165
                self.board_locs[5] = 165, 165
                self.board_locs[6] = 320, 165
                self.board_locs[7] = 10, 320
                self.board_locs[8] = 165, 320
                self.board_locs[9] = 320, 320
                self.reset()

        def reset(self):
                self.board = pygame.image.load(self.board_image)

        def update(self, letter, move):
                if letter == 'X':
                        piece = self.x_piece
                elif letter == 'O':
                        piece = self.o_piece
                else:
                        return
                loc = None
                if isinstance(move, tuple):
                        if move == (0,0):
                                loc = self.board_locs[1]
                        elif move == (0,1):
                                loc = self.board_locs[2]
                        elif move == (0,2):
                                loc = self.board_locs[3]
                        elif move == (1,0):
                                loc = self.board_locs[4]
                        elif move == (1,1):
                                loc = self.board_locs[5]
                        elif move == (1,2):
                                loc = self.board_locs[6]
                        elif move == (2,0):
                                loc = self.board_locs[7]
                        elif move == (2,1):
                                loc = self.board_locs[8]
                        elif move == (2,2):
                                loc = self.board_locs[9]
                if isinstance(move, int):
                        loc = self.board_locs[move]
                if loc:
                        self.board.blit(piece, loc)

        def hilite(self, loc):
                self.board.blit(self.blank, loc)

class Screen_Item(object):
        
        def __init__(self, name, pos_x=0, pos_y=0, image_file=None, hi_file=None,
                     callback=None, callback_args=None):
                self.name = name
                self.item_loc = pos_x, pos_y
                self.pos_x = pos_x
                self.pos_y = pos_y
                self.image_file = image_file
                self.hi_file = hi_file
                if image_file:
                        self.item_b = pygame.image.load(image_file)
                        self.item_rect = self.item_b.get_rect()
                        self.item_rect.top = self.pos_x
                        self.item_rect.left = self.pos_y
                if hi_file:
                        self.item_hi = pygame.image.load(hi_file)
                self.callback = callback
                self.callback_args = callback_args


class Display(ttt_internals.Display):

        def init(self):
                pygame.init()
                self.size = self.width, self.height = 1024, 768
                self.black = 0, 0, 0
                self.screen = pygame.display.set_mode(self.size)
                self.in_progress_msg = None
                self.result = None
                self.fixtures = {}
                self.fixtures['start'] = Screen_Item('start', pos_x=10, pos_y=32,
                                      image_file='start_button_5s.jpeg',
                                      hi_file='start_button_5s-h.png',
                                      callback=self.start,
                                      callback_args={})
                self.fixtures['X'] = Screen_Item('X', pos_x=10, pos_y=150,
                                      image_file='X_button_2s.jpg',
                                      hi_file='X_button_2s-h.png',
                                      callback=self.toggle_player,
                                      callback_args={'player':'player1', 'letter':'X'})
                self.fixtures['O'] = Screen_Item('O', pos_x=10, pos_y=255,
                                      image_file='O_button_1s.jpg',
                                      hi_file='O_button_1s-h.png',
                                      callback=self.toggle_player,
                                      callback_args={'player':'player2', 'letter':'O'})
                self.fixtures['reset'] = Screen_Item('reset', pos_x=10, pos_y=683,
                                      image_file='reset_button_1s.jpg',
                                      hi_file='reset_button_1s-h.png',
                                      callback=self.reset_game,
                                      callback_args={})
                self.fixtures['quit'] = Screen_Item('quit', pos_x=914, pos_y=26,
                                      image_file='quit_button_6.png',
                                      hi_file='quit_button_6-h.png',
                                      callback=self.quit,
                                      callback_args={})
                self.fixtures['human_player1'] = Screen_Item('player1', pos_x=85, pos_y=150,
                                      image_file='player_1-6.png',
                                      hi_file='player_1-6h2.png',
                                      callback=None,
                                      callback_args={})
                self.fixtures['computer_player1'] = Screen_Item('computer', pos_x=85, pos_y=150,
                                      image_file='computer-1.png',
                                      hi_file='computer-1h2.png',
                                      callback=None,
                                      callback_args={})
                self.fixtures['player1'] = self.fixtures['human_player1']
                self.fixtures['human_player2'] = Screen_Item('player2', pos_x=85, pos_y=255,
                                      image_file='player_2-1.png',
                                      hi_file='player_2-1h2.png',
                                      callback=None,
                                      callback_args={})
                self.fixtures['computer_player2'] = Screen_Item('computer', pos_x=85, pos_y=255,
                                      image_file='computer-1.png',
                                      hi_file='computer-1h2.png',
                                      callback=None,
                                      callback_args={})
                self.fixtures['player2'] = self.fixtures['computer_player2']
                self.fixtures['new_game'] = Screen_Item('new_game', pos_x=490, pos_y=130,
                                      image_file='new_game.png',
                                      hi_file=None,
                                      callback=None,
                                      callback_args={})
                self.fixtures['game_over'] = Screen_Item('game_over', pos_x=490, pos_y=130,
                                      image_file='game_over.png',
                                      hi_file=None,
                                      callback=None,
                                      callback_args={})
                self.fixtures['game_stopped'] = Screen_Item('game_stopped', pos_x=490, pos_y=130,
                                      image_file='game_stopped.png',
                                      hi_file=None,
                                      callback=None,
                                      callback_args={})
                self.fixtures['player1_wins'] = Screen_Item('player1_wins', pos_x=480, pos_y=680,
                                      image_file='player_1_wins.png',
                                      hi_file=None,
                                      callback=None,
                                      callback_args={})
                self.fixtures['player2_wins'] = Screen_Item('player2_wins', pos_x=480, pos_y=680,
                                      image_file='player_2_wins.png',
                                      hi_file=None,
                                      callback=None,
                                      callback_args={})
                self.fixtures['computer_wins'] = Screen_Item('computer_wins', pos_x=480, pos_y=680,
                                      image_file='computer_wins.png',
                                      hi_file=None,
                                      callback=None,
                                      callback_args={})
                self.fixtures['draw'] = Screen_Item('draw', pos_x=480, pos_y=680,
                                      image_file='draw.png',
                                      hi_file=None,
                                      callback=None,
                                      callback_args={})
                self.pg_board = PG_Board(pos_x=400, pos_y=200,
                                 board_image="board_5_l.jpg",
                                 x_image="X_button_2-2.png",
                                 o_image="O_button_1.png")
                base_x, base_y = self.pg_board.board_loc
                for i in range(1,10):
                        name = 'board_loc_' + str(i)
                        x_inc, y_inc = self.pg_board.board_locs[i]
                        pos_x = base_x + x_inc
                        pos_y = base_y + y_inc
                        self.fixtures[name] = Screen_Item(name, pos_x=pos_x, pos_y=pos_y,
                                        image_file="blank.png",
                                        hi_file=None,
                                        callback=self.update,
                                        callback_args={'loc':name})
                self.reset_game()

        def start(self, **args):
                if self.in_progress_msg != 'new_game':
                        self.reset_game()
                self.in_progress_msg = None

        def reset_game(self, **args):
                self.board.reset()
                self.active_player = self.player1
                self.pg_board.reset()
                self.in_progress_msg = 'new_game'
                self.result = None
                self.redraw_screen()

        def quit(self, **args):
                sys.exit(0)

        def toggle_player(self, **args):
                if args['player'] == 'player1':
                        working_item = self.player1
                else:
                        working_item = self.player2
                if working_item.player_type == 'human':
                        new_type = 'computer'
                        working_item = computer_player.Player(args['player'],
                                                              args['letter'],
                                                              self.board)
                else:
                        new_type = 'human'
                        working_item = ttt_internals.Player(args['player'],
                                                            args['letter'],
                                                            self.board)
                if args['player'] == 'player1':
                        self.player1 = working_item
                        self.board.set_player1(working_item)
                else:
                        self.player2 = working_item
                        self.board.set_player2(working_item)
                new_player_key = new_type + '_' + args['player']
                self.fixtures[args['player']] = self.fixtures[new_player_key]
                if not self.in_progress_msg:
                        self.in_progress_msg = 'game_stopped'
                self.redraw_screen()

        def get_current_item(self):
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for k,v in self.fixtures.iteritems():
                        # if the pointer is inside the rectangle that defines the object
                        if (mouse_x > v.item_rect.top and
                            mouse_x < v.item_rect.bottom and
                            mouse_y > v.item_rect.left and
                            mouse_y < v.item_rect.right):
                                return self.fixtures[v.name]
        
        def check_win(self):
                winner = self.board.check_win()
                if not winner or (isinstance(winner, str) and winner == 'draw'):
                        return winner
                if isinstance(winner, ttt_internals.Player):
                        if winner.letter == 'X':
                                return 'player1'
                        if winner.letter == 'O':
                                return 'player2'
                return None

        def mouse_click(self):
                button1, button2, button3 = pygame.mouse.get_pressed()
                if not button1:
                        return
                item = self.get_current_item()
                if item and item.callback:
                        item.callback(**item.callback_args)
                self.redraw_screen()

        def redraw_screen(self):
                self.screen.fill(self.black) # clear the screen
                # first everything that hilites because of cursor position
                cur_item = self.get_current_item()
                for f in ['start', 'X', 'O', 'reset', 'quit']:
                        if cur_item and self.fixtures[f].name == cur_item.name:
                                self.screen.blit(self.fixtures[f].item_hi, self.fixtures[f].item_loc)
                        else:
                                self.screen.blit(self.fixtures[f].item_b, self.fixtures[f].item_loc)
                # next board locations that are unused
                for i in range(1,10):
                        if self.board.data[self.board.board_locs[i]]: # if loc filled
                                continue
                        if cur_item == 'board_loc_' + str(i):
                                self.pg_board.hilite(self.pg_board.board_locs[i])
                                break
                # next the items that hilite based on active_player
                for f in ['player1', 'player2']:
                        if self.fixtures[f].name == self.active_player.name:
                                self.screen.blit(self.fixtures[f].item_hi, self.fixtures[f].item_loc)
                        else:
                                self.screen.blit(self.fixtures[f].item_b, self.fixtures[f].item_loc)
                # next the board
                self.screen.blit(self.pg_board.board, self.pg_board.board_loc)
                # next the status messages
                if self.in_progress_msg:
                        msg = self.fixtures[self.in_progress_msg]
                        self.screen.blit(msg.item_b, msg.item_loc)
                if self.result:
                        msg = self.fixtures[self.result]
                        self.screen.blit(msg.item_b, msg.item_loc)
                pygame.display.flip()

        def update(self, **kwargs):
                if kwargs:
                        if isinstance(kwargs['loc'], str):
                                index = int(kwargs['loc'][-1])
                        else:
                                index = kwargs['loc']
                        self.board.update(self.active_player, self.board.board_locs[index])
                        self.pg_board.update(self.active_player.letter, self.board.board_locs[index])
                        self.toggle_active_player()
                        self.result = self.check_win()
                        if self.result == 'draw':
                                self.in_progress_msg = self.result
                        elif self.result in ['player1', 'player2', 'computer']:
                                self.result += '_wins'
                                self.in_progress_msg = 'game_over'
                self.redraw_screen()

        def mainloop(self):
                pygame.event.set_blocked(pygame.MOUSEMOTION)
                while 1:
                        if self.active_player.player_type == 'computer':
                                move = self.active_player.choose()
                                for i in range(1,10):
                                        if self.board.board_locs[i] == move:
                                                self.update(loc=i)
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        sys.exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                        self.mouse_click()
                        self.redraw_screen()

