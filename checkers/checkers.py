"""
Definition of a game of checkers
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Set, Union

BOARD_SIZE = 8


@dataclass(frozen=True)
class Location:
    row: int
    col: int


@dataclass(frozen=True)
class Move:
    start: Location
    end: Location


class Player(Enum):
    RED = "R"
    WHITE = "W"


class Piece:
    def __init__(self, player: Player, king: bool = False):
        self.player: Player = player
        self.king: bool = king


class CheckersGameState:
    board: List[List[Union[Piece, None]]] = []
    turn: Player = Player.WHITE

    def __init__(self):
        self.board = [[]] * BOARD_SIZE
        for row in range(BOARD_SIZE):
            self.board[row] = [None] * BOARD_SIZE

        self.reset()

    def reset(self):
        """
            The game starts like this
            _ R _ R _ R _ R
            R _ R _ R _ R _
            _ R _ R _ R _ R
            _ _ _ _ _ _ _ _
            _ _ _ _ _ _ _ _
            W _ W _ W _ W _
            _ W _ W _ W _ W
            W _ W _ W _ W _
        """
        for row in range(3):
            for col in range(BOARD_SIZE):
                self.board[row][col] = None if (row + col) % 2 == 0 else Piece(player=Player.RED)
        for row in range(BOARD_SIZE - 3, BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.board[row][col] = None if (row + col) % 2 == 0 else Piece(player=Player.WHITE)

    def get_possible_moves(self) -> Set[Move]:
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                pass

    def _get_possible_moves_for_chip(self, row: int, col: int) -> Set[Move]:
        pass

    def get_single_unit_moves(self, start_location: Location, piece: Piece) -> Set[Move]:
        """A single unit move is a move that goes col±1, row±1. It's a move that's not eating."""

        next_locations: Set[Location] = set()
        # single unit moves, no eating
        if piece.king:
            next_locations = {
                Location(start_location.row - 1, start_location.col - 1),
                Location(start_location.row - 1, start_location.col + 1),
                Location(start_location.row + 1, start_location.col - 1),
                Location(start_location.row + 1, start_location.col + 1)
            }
        elif piece.player == Player.WHITE:
            # white non-king must move in decreasing row direction
            next_locations = {Location(start_location.row - 1, start_location.col - 1),
                              Location(start_location.row - 1, start_location.col + 1)}
        elif piece.player == Player.RED:
            # red non-king must move in the increasing row direction
            next_locations = {Location(start_location.row + 1, start_location.col - 1),
                              Location(start_location.row + 1, start_location.col + 1)}

        # these moves are only valid if there's nobody in the spot you want to move to
        return set([Move(start=start_location, end=end_location) for end_location in next_locations if
                    self.is_location_on_board(end_location) and
                    self.board[end_location.row][end_location.col] is None])

    def get_eating_moves(self, start_location: Location, piece: Piece) -> Set[Move]:
        """An eating move is a move that jumps over another piece and captures them."""
        next_locations: Set[Location] = set()
        # eating moves
        if piece.king:
            next_locations = {
                Location(start_location.row - 2, start_location.col - 2),
                Location(start_location.row - 2, start_location.col + 2),
                Location(start_location.row + 2, start_location.col - 2),
                Location(start_location.row + 2, start_location.col + 2)
            }
        elif piece.player == Player.WHITE:
            # white non-king must move in decreasing row direction
            next_locations = {Location(start_location.row - 2, start_location.col - 2),
                              Location(start_location.row - 2, start_location.col + 2)}
        elif piece.player == Player.RED:
            # red non-king must move in the increasing row direction
            next_locations = {Location(start_location.row + 2, start_location.col - 2),
                              Location(start_location.row + 2, start_location.col + 2)}

        moves: Set[Move] = set()
        for end_location in next_locations:
            middle_location = Location(row=(start_location.row + end_location.row) // 2,
                                       col=(start_location.col + end_location.col) // 2)
            if not self.is_location_on_board(end_location):
                continue
            # you can only eat it if the spot you're jumping over is the opposing player
            eaten_piece = self.board[middle_location.row][middle_location.col]
            if eaten_piece is not None and eaten_piece.player != piece.player:
                moves.add(Move(start=start_location, end=end_location))

        return moves

    def is_location_on_board(self, location: Location):
        return not (location.row < 0 or
                    location.col < 0 or
                    location.row > BOARD_SIZE - 1 or
                    location.col > BOARD_SIZE - 1 or
                    location.row < 0 or
                    location.col < 0 or
                    location.row > BOARD_SIZE - 1 or
                    location.col > BOARD_SIZE - 1)

    def get_moves_for_piece(self, location: Location, piece: Piece) -> Set[Move]:
        return (self.get_eating_moves(start_location=location, piece=piece) |
                self.get_single_unit_moves(start_location=location, piece=piece))

    def is_move_valid(self, move: Move):
        piece = self.board[move.start.row][move.start.col]
        if piece is None:
            return False
        return move in self.get_moves_for_piece(location=move.start, piece=piece)
