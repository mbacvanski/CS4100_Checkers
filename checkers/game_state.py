from __future__ import annotations

from collections import namedtuple
from copy import deepcopy
from typing import List, Tuple

from checkers import *

MovesForPiece = namedtuple("MovesForPiece", "x y actions")
Action = namedtuple("Action", "from_x from_y to_x to_y")
PlayerColor = Tuple


# PlayerColor = Union[BLUE, RED]


class GameState:
    board: Board = None
    game: Game = None
    current_player_color: Color = None
    depth: int = 0

    def __init__(self, board: Board, game: Game, color: PlayerColor, depth: int = 0):
        self.board = board
        self.game = game
        self.current_player_color = color
        self.depth = depth

    def is_terminal(self) -> bool:
        pass

    def next_actions(self) -> List[Action]:
        """
        Returns a list of [(from_x, from_to, to_x, to_y), ...]
        """
        actions: List[Action] = []
        moves: List[MovesForPiece] = self._generate_move(self.board)
        for move_from_x, move_from_y, move_tos in moves:
            for move_to in move_tos:
                actions.append(Action(move_from_x, move_from_y, move_to[0], move_to[1]))

        return actions

    # Successor function
    def next_state(self, action: Action) -> GameState:
        next_board = deepcopy(self.board)  # makes a copy of the board

        from_coord = (action[0], action[1])
        to_coord = (action[2], action[3])
        self._run_action_on_board(next_board, from_coord, to_coord)  # modify the board clone

        next_state = GameState(
            board=next_board,
            game=self.game,
            color=_next_player_color(self.current_player_color),
            depth=self.depth + 1,
        )
        return next_state

    def value(self) -> float:
        return self._piece2val(self.board, self.current_player_color)

    def _piece2val(self, board, color):
        score = 0
        for i in range(8):
            for j in range(8):
                occupant = board.location(i, j).occupant
                if occupant is not None:
                    if occupant.current_player_color == color:
                        score += occupant.value
                    else:
                        score -= occupant.value
        return score

    def _generate_move(self, board) -> List[MovesForPiece]:
        for i in range(8):
            for j in range(8):
                if (board.legal_moves(i, j, self.game.hop) != []
                        and board.location(i, j).occupant != None
                        and board.location(i, j).occupant.color == self.game.turn):
                    yield MovesForPiece(i, j, board.legal_moves(i, j, self.game.hop))

    def _run_action_on_board(self, board, current_pos, final_pos, hop=False):
        if hop == False:
            if board.location(final_pos[0], final_pos[1]).occupant != None and board.location(final_pos[0], final_pos[
                1]).occupant.color == self.game.turn:
                current_pos = final_pos

            elif current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):
                board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                if final_pos not in board.adjacent(current_pos[0], current_pos[1]):
                    # print("REMOVE", current_pos, final_pos)
                    board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                       2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)
                    hop = True
                    current_pos = final_pos
                    final_pos = board.legal_moves(current_pos[0], current_pos[1], True)
                    if final_pos != []:
                        # print("HOP in Action", current_pos, final_pos)
                        self._run_action_on_board(board, current_pos, final_pos[0], hop=True)
        else:
            # print(current_pos, final_pos)
            if current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1], hop):
                board.move_piece(current_pos[0], current_pos[1], final_pos[0], final_pos[1])
                board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) // 2,
                                   current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

            if board.legal_moves(final_pos[0], final_pos[1], self.game.hop) == []:
                return
            else:
                current_pos = final_pos
                final_pos = board.legal_moves(current_pos[0], current_pos[1], True)
                if final_pos != []:
                    # print("HOP in Action", current_pos, final_pos)
                    self._run_action_on_board(board, current_pos, final_pos[0], hop=True)


def _next_player_color(color: PlayerColor) -> PlayerColor:
    if color == BLUE:
        return RED
    elif color == RED:
        return BLUE
