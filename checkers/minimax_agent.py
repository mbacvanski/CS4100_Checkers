import random
from typing import Tuple, Union

from checkers import Game
from game_state import Action, GameState, PlayerColor, _next_player_color, piece2val


class MinimaxAgent:
    color: PlayerColor = None  # which color does this agent play for
    game: Game = None
    depth_limit: int = 0

    def __init__(self, color: PlayerColor, game: Game, depth: int, eval_fn=piece2val):
        self.color = color
        self.game = game
        self.depth_limit = depth
        self.adversary_color = _next_player_color(self.color)
        self.eval_fn = eval_fn

    def make_move(self):
        move = self._get_move(start_from=self.game.last_hop_to)
        if move is not None:
            self._action(current_pos=(move.from_x, move.from_y), final_pos=(move.to_x, move.to_y),
                         board=self.game.board)
        else:
            self.game.end_turn()

    def _get_move(self, start_from=None):
        starting_state = GameState(
            game=self.game,
            eval_fn=self.eval_fn,
            start_from=start_from,
        )
        return self.minimax(starting_state=starting_state, depth=self.depth_limit)[1]

    def minimax(self, starting_state: GameState, depth=10, eval_fn=None) -> Tuple[float, Union[Action, None]]:
        if starting_state.game.endit:
            return (1 if starting_state.game.whoWon() == self.color else -1), None

        if starting_state.depth > depth:
            # return self.evaluation_function(starting_state), None
            return starting_state.value(), None

        if starting_state.game.turn == self.color:
            # print(f'running max on depth, {starting_state.depth}')
            return self.run_max(starting_state)
        else:
            # print(f'running min on depth, {starting_state.depth}')
            return self.run_min(starting_state)

    def run_max(self, state: GameState) -> Tuple[float, Union[Action, None]]:
        max_value = float('-inf')
        max_action = None

        for action in state.next_actions():
            new_game_state = state.next_state(action)
            value, _ = self.minimax(new_game_state, self.depth_limit)
            if value > max_value:
                max_value = value
                max_action = action
            elif value == max_value and bool(random.randint(0, 1)):
                max_value = value
                max_action = action

        if max_action is None:  # if you can't take any actions, your value is 0
            return 0, None
        return max_value, max_action

    def run_min(self, state: GameState) -> Tuple[float, Union[Action, None]]:
        min_value = float('inf')
        min_action = None

        for action in state.next_actions():
            new_game_state = state.next_state(action)
            value, _ = self.minimax(new_game_state, self.depth_limit)
            if value < min_value:
                min_value = value
                min_action = action
            elif value == min_value and bool(random.randint(0, 1)):
                min_value = value
                min_action = action
        if min_action is None:  # if you can't take any actions, your value is 0
            return 0, None
        return min_value, min_action

    def _action(self, current_pos, final_pos, board):
        if current_pos is None:
            self.game.end_turn()

        if board.location(final_pos[0], final_pos[1]).occupant is not None and board.location(final_pos[0], final_pos[
            1]).occupant.color == self.game.turn:
            current_pos = final_pos

        elif current_pos is not None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):
            board.move_piece(
                current_pos[0], current_pos[1], final_pos[0], final_pos[1])

            if final_pos not in board.adjacent(current_pos[0], current_pos[1]):
                board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                   2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

                self.game.hop = True
                self.game.last_hop_to = final_pos
            else:  # not a hop
                self.game.end_turn()
                # self.game.turn = self.adversary_color
