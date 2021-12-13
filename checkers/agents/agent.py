from abc import ABC, abstractmethod
from typing import Tuple

from checkers import BLUE, Game, GameState, PlayerColor, RED
from game_state import Action


class Agent(ABC):
    color: PlayerColor = None  # which color does this agent play for
    game: Game = None

    def __init__(self, color: PlayerColor, game: Game, eval_fn):
        self.color = color
        self.game = game
        self.adversary_color = _next_player_color(self.color)
        self.eval_fn = eval_fn

    def make_move(self):
        move: Action = self._get_move(start_from=self.game.state.last_hop_to)
        if move is not None:
            self._action(action=move, state=self.game.state)
        else:
            self.game.end_turn()

    @abstractmethod
    def _get_move(self, start_from: Tuple = None):
        pass

    def _action(self, action: Action, state: GameState):
        current_pos, final_pos = (action.from_x, action.from_y), (action.to_x, action.to_y)

        if (state.board.location(final_pos[0], final_pos[1]).occupant is not None
                and state.board.location(final_pos[0], final_pos[1]).occupant.color == state.turn):
            state.end_turn()
            return

        state.board.move_piece(current_pos[0], current_pos[1], final_pos[0], final_pos[1])
        if final_pos not in state.board.adjacent(current_pos[0], current_pos[1]):  # hop
            state.board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) // 2,
                                     current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

            if state.board.legal_moves(final_pos[0], final_pos[1], mid_hop=True):
                # More legal moves to make, we are mid-hop
                state.mid_hop = True
            else:
                # No more legal moves now
                state.end_turn()
        else:
            state.end_turn()


def _next_player_color(color: PlayerColor) -> PlayerColor:
    if color == BLUE:
        return RED
    elif color == RED:
        return BLUE
