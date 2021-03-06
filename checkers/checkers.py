"""
checkers.py

A simple checkers engine written in Python with the pygame 1.9.1 libraries.

Here are the rules I am using: http://boardgames.about.com/cs/checkersdraughts/ht/play_checkers.htm

Functionalities include:

- Having the pieces and board drawn to the screen

- The ability to move pieces by clicking on the piece you want to move, then clicking on the square you would
  like to move to. You can change you mind about the piece you would like to move, just click on a new piece of yours.

- Knowledge of what moves are legal. When moving pieces, you'll be limited to legal moves.

- Capturing

- DOUBLE capturing etc.

- Legal move and captive piece highlighting

- Turn changes

- Automatic kinging and the ability for them to move backwords

- Automatic check for and end game.

- A silky smoooth 60 FPS!
"""

import sys
from collections import namedtuple
from copy import deepcopy
from typing import List, Tuple

import pygame
from pygame.locals import *

pygame.font.init()

##COLORS##
#         R    G    B
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
HIGH = (160, 190, 255)
PlayerColor = Tuple

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"


class Board:
    def __init__(self):
        self.matrix = self.new_board()

    def new_board(self):
        """
        Create a new board matrix.
        """

        # initialize squares and place them in matrix

        matrix = [[None] * 8 for i in range(8)]

        # The following code block has been adapted from
        # http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py
        for x in range(8):
            for y in range(8):
                if (x % 2 != 0) and (y % 2 == 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 != 0) and (y % 2 != 0):
                    matrix[y][x] = Square(BLACK)
                elif (x % 2 == 0) and (y % 2 != 0):
                    matrix[y][x] = Square(WHITE)
                elif (x % 2 == 0) and (y % 2 == 0):
                    matrix[y][x] = Square(BLACK)

        # initialize the pieces and put them in the appropriate squares

        for x in range(8):
            for y in range(3):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(RED)
            for y in range(5, 8):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(BLUE)

        return matrix

    def get_locations_by_color(self, color: PlayerColor) -> List[Tuple[int, int]]:
        locations = []
        for x in range(8):
            for y in range(8):
                if self.matrix[x][y] and self.matrix[x][y].occupant and self.matrix[x][y].occupant.color == color:
                    locations.append((x, y))

        return locations

    def get_king_locations(self, color: PlayerColor) -> List[Tuple[int, int]]:
        locations = []
        for x in range(8):
            for y in range(8):
                if (self.matrix[x][y] and self.matrix[x][y].occupant
                        and self.matrix[x][y].occupant.color == color and self.matrix[x][y].occupant.king):
                    locations.append((x, y))

        return locations

    def board_string(self, board):
        """
        Takes a board and returns a matrix of the board space colors. Used for testing new_board()
        """

        board_string = [[None] * 8] * 8

        for x in range(8):
            for y in range(8):
                if board[x][y].color == WHITE:
                    board_string[x][y] = "WHITE"
                else:
                    board_string[x][y] = "BLACK"

        return board_string

    def rel(self, dir, x, y):
        """
        Returns the coordinates one square in a different direction to (x,y).

        ===DOCTESTS===

        >>> board = Board()

        >>> board.rel(NORTHWEST, (1,2))
        (0,1)

        >>> board.rel(SOUTHEAST, (3,4))
        (4,5)

        >>> board.rel(NORTHEAST, (3,6))
        (4,5)

        >>> board.rel(SOUTHWEST, (2,5))
        (1,6)
        """
        if dir == NORTHWEST:
            return (x - 1, y - 1)
        elif dir == NORTHEAST:
            return (x + 1, y - 1)
        elif dir == SOUTHWEST:
            return (x - 1, y + 1)
        elif dir == SOUTHEAST:
            return (x + 1, y + 1)
        else:
            return 0

    def adjacent(self, x, y):
        """
        Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
        """

        return [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y), self.rel(SOUTHWEST, x, y),
                self.rel(SOUTHEAST, x, y)]

    def location(self, x, y):
        """
        Takes a set of coordinates as arguments and returns self.matrix[x][y]
        This can be faster than writing something like self.matrix[coords[0]][coords[1]]
        """
        x = int(x)
        y = int(y)
        return self.matrix[x][y]

    def blind_legal_moves(self, x, y):
        """
        Returns a list of blind legal move locations from a set of coordinates (x,y) on the board.
        If that location is empty, then blind_legal_moves() return an empty list.
        """
        # print(x)
        if self.matrix[x][y].occupant != None:
            if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == BLUE:
                blind_legal_moves = [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y)]

            elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == RED:
                blind_legal_moves = [self.rel(SOUTHWEST, x, y), self.rel(SOUTHEAST, x, y)]

            else:
                blind_legal_moves = [self.rel(NORTHWEST, x, y), self.rel(NORTHEAST, x, y), self.rel(SOUTHWEST, x, y),
                                     self.rel(SOUTHEAST, x, y)]

        else:
            blind_legal_moves = []

        return blind_legal_moves

    def legal_moves(self, x, y, mid_hop=False):
        """
        Returns a list of legal move locations from a given set of coordinates (x,y) on the board.
        If that location is empty, then legal_moves() returns an empty list.
        """
        # print(x, y)
        blind_legal_moves = self.blind_legal_moves(x, y)
        # print('BLind Legal moves', blind_legal_moves)
        legal_moves = []

        if not mid_hop:
            for move in blind_legal_moves:
                if not mid_hop:
                    if self.on_board(move[0], move[1]):
                        if self.location(move[0], move[1]).occupant is None:
                            legal_moves.append(move)

                        elif (self.location(move[0], move[1]).occupant.color != self.location(x, y).occupant.color
                              and self.on_board(move[0] + (move[0] - x), move[1] + (move[1] - y))
                              and self.location(move[0] + (move[0] - x), move[1] + (move[1] - y)).occupant is None):
                            # is this location filled by an enemy piece?
                            legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        else:  # hop == True
            for move in blind_legal_moves:
                if self.on_board(move[0], move[1]) and self.location(move[0], move[1]).occupant is not None:
                    if (self.location(move[0], move[1]).occupant.color != self.location(x, y).occupant.color
                            and self.on_board(move[0] + (move[0] - x), move[1] + (move[1] - y))
                            and self.location(move[0] + (move[0] - x), move[1] + (move[1] - y)).occupant is None):
                        # is this location filled by an enemy piece?
                        legal_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        return legal_moves

    def remove_piece(self, x, y):
        """
        Removes a piece from the board at position (x,y).
        """
        self.matrix[x][y].occupant = None

    def move_piece(self, start_x, start_y, end_x, end_y):
        """
        Move a piece from (start_x, start_y) to (end_x, end_y).
        """

        self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
        self.remove_piece(start_x, start_y)

        self.king(end_x, end_y)

    def is_end_square(self, coords):
        """
        Is passed a coordinate tuple (x,y), and returns true or
        false depending on if that square on the board is an end square.

        ===DOCTESTS===

        >>> board = Board()

        >>> board.is_end_square((2,7))
        True

        >>> board.is_end_square((5,0))
        True

        >>>board.is_end_square((0,5))
        False
        """

        if coords[1] == 0 or coords[1] == 7:
            return True
        else:
            return False

    def on_board(self, x, y):
        """
        Checks to see if the given square (x,y) lies on the board.
        If it does, then on_board() return True. Otherwise it returns false.

        ===DOCTESTS===
        # >>> board = Board()
        #
        # >>> board.on_board((5,0)):
        # True
        #
        # >>> board.on_board(-2, 0):
        # False
        #
        # >>> board.on_board(3, 9):
        # False
        """

        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        else:
            return True

    def king(self, x, y):
        """
        Takes in (x,y), the coordinates of square to be considered for kinging.
        If it meets the criteria, then king() kings the piece in that square and kings it.
        """
        if self.location(x, y).occupant is not None:
            if (self.location(x, y).occupant.color == BLUE and y == 0) or (
                    self.location(x, y).occupant.color == RED and y == 7):
                self.location(x, y).occupant.crown()

    def repr_matrix(self):
        for j in range(8):
            for i in range(8):
                if self.matrix[i][j].occupant is not None:
                    if self.matrix[i][j].occupant.color == BLUE:
                        print('B', end=" ")
                    else:
                        print('R', end=" ")
                else:
                    print('X', end=" ")
            print('')


class GameState:
    def __init__(self, board=None, game_over=None, turn=None, mid_hop=None, last_hop_to=None, move_count=None):
        self.board: Board = board if board is not None else Board()
        self.game_over = game_over if game_over is not None else False
        self.turn = turn if turn is not None else BLUE
        self.mid_hop = mid_hop if mid_hop is not None else False  # are we in the middle of a hop?
        self.last_hop_to = last_hop_to if last_hop_to is not None else None
        self.move_count = move_count if move_count is not None else 0

    def __deepcopy__(self, memodict={}):
        g = GameState(board=deepcopy(self.board, memodict), game_over=self.game_over, turn=self.turn,
                      mid_hop=self.mid_hop,
                      last_hop_to=self.last_hop_to, move_count=self.move_count)
        return g

    def whoWon(self):
        num_red = 0
        num_blue = 0
        for i in range(8):
            for j in range(8):
                occupant = self.board.location(i, j).occupant
                if occupant is None:
                    continue

                if occupant.color == RED:
                    num_red += 1
                else:
                    num_blue += 1

        if num_red == 0 and num_blue > 0:
            return BLUE
        elif num_blue == 0 and num_red > 0:
            return RED
        return None

    def end_turn(self):
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE

        self.mid_hop = False
        self.last_hop_to = None
        self.move_count += 1

        if self.is_game_over():
            self.game_over = True

    def is_game_over(self):
        """
        Checks to see if either player has run out of moves or pieces. If so, then return True. Else return False.
        """
        red_has_moves, blue_has_moves = False, False

        for x in range(8):
            for y in range(8):
                # if (self.board.location(x, y).color == BLACK and self.board.location(x, y).occupant is not None and
                #         self.board.location(x, y).occupant.color == self.turn):
                location = self.board.location(x, y)
                if location.color == BLACK and location.occupant is not None and self.board.legal_moves(x, y):
                    if location.occupant.color == BLUE:
                        blue_has_moves = True
                    else:
                        red_has_moves = True

        # if only one of them has moves, then the game is over
        return not (red_has_moves and blue_has_moves)


class Game:
    """
    The main game control.
    """
    selected_legal_moves = []
    mouse_pos = None
    selected_piece = None
    loop_mode = False

    def __init__(self, loop_mode: bool, state: GameState = None):
        self.state = state if state is not None else GameState()
        self.graphics = Graphics()
        self.loop_mode = loop_mode

    def setup(self):
        """Draws the window and board at the beginning of the game"""
        self.graphics.setup_window()

    # TODO: use this inside player_turn
    def _action(self, current_pos, final_pos, board: Board):
        if current_pos is None:
            self.end_turn()

        if board.location(final_pos[0], final_pos[1]).occupant is not None and board.location(final_pos[0], final_pos[
            1]).occupant.color == self.state.turn:
            current_pos = final_pos

        elif current_pos is not None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):
            board.move_piece(
                current_pos[0], current_pos[1], final_pos[0], final_pos[1])

            if final_pos not in board.adjacent(current_pos[0], current_pos[1]):
                board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                   2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

                self.mid_hop = True
                self.last_hop_to = final_pos
            else:  # not a hop
                self.end_turn()
                # self.game.turn = self.adversary_color

    def player_turn(self):
        """
        The event loop. This is where events are triggered
        (like a mouse click) and then effect the game state.
        """
        mouse_pos = tuple(map(int, pygame.mouse.get_pos()))
        self.mouse_pos = tuple(
            map(int, self.graphics.board_coords(mouse_pos[0], mouse_pos[1])))  # what square is the mouse in?
        if self.selected_piece is not None:
            self.selected_legal_moves = self.state.board.legal_moves(x=self.selected_piece[0],
                                                                     y=self.selected_piece[1],
                                                                     mid_hop=self.state.mid_hop)

        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate_game()

            if event.type == MOUSEBUTTONDOWN:
                # print(self.hop)
                if not self.state.mid_hop:
                    if (self.state.board.location(self.mouse_pos[0], self.mouse_pos[1]).occupant is not None and
                            self.state.board.location(self.mouse_pos[0],
                                                      self.mouse_pos[1]).occupant.color == self.state.turn):
                        self.selected_piece = self.mouse_pos

                    elif self.selected_piece is not None and self.mouse_pos in self.state.board.legal_moves(
                            self.selected_piece[0], self.selected_piece[1]):
                        self.state.board.move_piece(start_x=self.selected_piece[0],
                                                    start_y=self.selected_piece[1],
                                                    end_x=self.mouse_pos[0],
                                                    end_y=self.mouse_pos[1])

                        if self.mouse_pos not in self.state.board.adjacent(self.selected_piece[0],
                                                                           self.selected_piece[1]):
                            self.state.board.remove_piece(
                                self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2,
                                self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

                            self.state.mid_hop = True
                            self.selected_piece = self.mouse_pos
                        else:
                            self.end_turn()

                if self.state.mid_hop:
                    if self.selected_piece is not None and self.mouse_pos in self.state.board.legal_moves(
                            self.selected_piece[0],
                            self.selected_piece[1],
                            self.state.mid_hop):
                        self.state.board.move_piece(self.selected_piece[0], self.selected_piece[1], self.mouse_pos[0],
                                                    self.mouse_pos[1])
                        self.state.board.remove_piece(
                            self.selected_piece[0] + (self.mouse_pos[0] - self.selected_piece[0]) // 2,
                            self.selected_piece[1] + (self.mouse_pos[1] - self.selected_piece[1]) // 2)

                    if not self.state.board.legal_moves(self.mouse_pos[0], self.mouse_pos[1], self.state.mid_hop):
                        self.end_turn()

                    else:
                        self.selected_piece = self.mouse_pos

    def update(self):
        """Calls on the graphics class to update the game display."""
        self.graphics.update_display(self.state.board, self.selected_legal_moves, self.selected_piece)

    def terminate_game(self):
        """Quits the program and ends the game."""
        pygame.quit()
        sys.exit()

    def main(self):
        """This executes the game and controls its flow."""
        self.setup()

        while True:  # main game loop
            self.player_turn()
            self.update()

    def end_turn(self):
        """
        End the turn. Switches the current player.
        end_turn() also checks for and game and resets a lot of class attributes.
        """
        self.state.end_turn()
        self.selected_piece = None
        self.selected_legal_moves = []

        if self.state.is_game_over():
            if self.state.whoWon() == BLUE:
                self.graphics.draw_message("BLUE WINS!")
            else:
                self.graphics.draw_message("RED WINS!")
            if not self.loop_mode:
                self.terminate_game()


class Graphics:
    def __init__(self):
        self.caption = "Checkers"

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.window_size = 600
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        self.background = pygame.image.load('resources/board.png')

        self.square_size = self.window_size // 8
        self.piece_size = self.square_size // 2

        self.message = False

    def setup_window(self):
        """
        This initializes the window and sets the caption at the top.
        """
        pygame.init()
        pygame.display.set_caption(self.caption)

    def update_display(self, board, legal_moves, selected_piece):
        """
        This updates the current display.
        """
        self.screen.blit(self.background, (0, 0))

        self.highlight_squares(legal_moves, selected_piece)
        self.draw_board_pieces(board)

        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)

        pygame.display.update()
        self.clock.tick(self.fps)

    def draw_board_squares(self, board):
        """
        Takes a board object and draws all of its squares to the display
        """
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen, board[x][y].color,
                                 (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )

    def draw_board_pieces(self, board):
        """
        Takes a board object and draws all of its pieces to the display
        """
        for x in range(8):
            for y in range(8):
                if board.matrix[x][y].occupant != None:
                    pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color,
                                       tuple(map(int, self.pixel_coords((x, y)))), int(self.piece_size))

                    if board.location(x, y).occupant.king == True:
                        # print("228->", self.screen, GOLD, self.pixel_coords((x, y)), self.piece_size // 1.7, self.piece_size // 4)
                        pygame.draw.circle(self.screen, GOLD, self.pixel_coords((x, y)), int(self.piece_size // 1.7),
                                           self.piece_size // 4)

    def pixel_coords(self, board_coords):
        """
        Takes in a tuple of board coordinates (x,y)
        and returns the pixel coordinates of the center of the square at that location.
        """
        return (
            board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

    def board_coords(self, pixel_x, pixel_y):
        """
        Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
        """
        return (pixel_x // self.square_size, pixel_y // self.square_size)

    def highlight_squares(self, squares, origin):
        """
        Squares is a list of board coordinates.
        highlight_squares highlights them.
        """
        for square in squares:
            pygame.draw.rect(self.screen, HIGH, (
                square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))

        if origin != None:
            pygame.draw.rect(self.screen, HIGH, (
                origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

    def draw_message(self, message):
        """
        Draws message to the screen.
        """
        self.message = True
        self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
        self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.window_size // 2, self.window_size // 2)


class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king
        self.value = 1

    def crown(self):
        self.king = True
        self.value = 2


class Square:
    def __init__(self, color, occupant=None):
        self.color = color  # color is either BLACK or WHITE
        self.occupant = occupant  # occupant is a Piece object


def _next_player_color(color: PlayerColor) -> PlayerColor:
    if color == BLUE:
        return RED
    elif color == RED:
        return BLUE


Action = namedtuple("Action", "from_x from_y to_x to_y")
