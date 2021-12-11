from __future__ import annotations

from collections import namedtuple
from typing import List, Tuple

from checkers import *

MovesForPiece = namedtuple("MovesForPiece", "x y actions")
Action = namedtuple("Action", "from_x from_y to_x to_y")
PlayerColor = Tuple


# PlayerColor = Union[BLUE, RED]

def piece2val(board: Board, color: PlayerColor):
    score = 0
    for i in range(8):
        for j in range(8):
            occupant = board.location(i, j).occupant
            if occupant is not None:
                if occupant.color == color:
                    score += 1
                else:
                    score -= 1
    return score


def piece2val_inv(board: Board, color: PlayerColor):
    badness = 0
    for i in range(8):
        for j in range(8):
            occupant = board.location(i, j).occupant
            if occupant is not None:
                if occupant.color == color:
                    badness -= 1
                else:
                    badness += 1

    # incentive to keep pieces in the back row to prevent opponent from becoming a king
    for i in range(0, 8, 2):
        occupant = board.location(i, 0).occupant
        if occupant is not None and occupant.color == color:
            badness -= occupant.value * 0.5

    return 24 - badness


def piece2val_favor_kings(board: Board, color: PlayerColor):
    score = 0
    for i in range(8):
        for j in range(8):
            occupant = board.location(i, j).occupant
            if occupant is not None:
                value = 1 if occupant.king else 5
                if occupant.color == color:
                    score += value
                else:
                    score -= value
    return score


class GameState:
    game: Game = None
    depth: int = 0
    eval_fn = piece2val
    start_from: Tuple = None

    def __init__(self, game: Game, depth: int = 0, eval_fn=piece2val, start_from: Tuple = None):
        self.game = game
        self.depth = depth
        self.eval_fn = eval_fn
        self.start_from = start_from

    def is_terminal(self) -> bool:
        return self.game.whoWon() is not None

    def next_actions(self) -> List[Action]:
        """
        Returns a list of [(from_x, from_to, to_x, to_y), ...]
        """
        actions: List[Action] = []
        moves: List[MovesForPiece] = []

        if self.start_from is not None:
            i, j = self.start_from
            moves = [MovesForPiece(i, j, self.game.board.legal_moves(i, j, self.game.hop))]
        else:
            moves = self._generate_moves()

        for move_from_x, move_from_y, move_tos in moves:
            for move_to in move_tos:
                actions.append(Action(move_from_x, move_from_y, move_to[0], move_to[1]))

        return actions

    # Successor function returns a new GameState object
    def next_state(self, action: Action) -> GameState:
        next_board = deepcopy(self.game.board)  # makes a copy of the board

        from_coord = (action[0], action[1])
        to_coord = (action[2], action[3])
        # self._run_action_on_board(next_board, from_coord, to_coord)  # modify the board clone

        next_game = deepcopy(self.game)
        next_game.board = next_board
        self._action(current_pos=from_coord, final_pos=to_coord, game=next_game)

        next_state = GameState(
            game=next_game,
            depth=self.depth + 1,
            eval_fn=self.eval_fn
        )
        return next_state

    def value(self) -> float:
        return self.eval_fn(self.game.board, self.game.turn)

    def _generate_moves(self) -> List[MovesForPiece]:
        for i in range(8):
            for j in range(8):
                if (self.game.board.legal_moves(i, j, self.game.hop) != []
                        and self.game.board.location(i, j).occupant is not None
                        and self.game.board.location(i, j).occupant.color == self.game.turn):
                    yield MovesForPiece(i, j, self.game.board.legal_moves(i, j, self.game.hop))

    def _action(self, current_pos, final_pos, game: Game):
        if current_pos is None:
            self.game.end_turn()

        if game.board.location(final_pos[0], final_pos[1]).occupant is not None \
                and game.board.location(final_pos[0], final_pos[1]).occupant.color == self.game.turn:
            current_pos = final_pos

        elif current_pos is not None and final_pos in game.board.legal_moves(current_pos[0], current_pos[1]):
            game.board.move_piece(
                current_pos[0], current_pos[1], final_pos[0], final_pos[1])

            if final_pos not in game.board.adjacent(current_pos[0], current_pos[1]):
                game.board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                        2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

                game.hop = True
                game.last_hop_to = final_pos
            else:  # not a hop
                game.end_turn()

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
