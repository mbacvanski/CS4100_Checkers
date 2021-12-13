import random
from typing import Tuple, Union

from checkers import Game, GameState
from game_state import Action, Node, PlayerColor, _next_player_color
from eval_fns import piece2val


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
        move: Action = self._get_move(start_from=self.game.state.last_hop_to)
        if move is not None:
            self._action(action=move, state=self.game.state)
        else:
            self.game.end_turn()

    def _get_move(self, start_from=None):
        starting_state = Node(
            state=self.game.state,
            eval_fn=self.eval_fn,
            start_from=start_from,
        )
        return self.minimax(starting_state=starting_state, depth=self.depth_limit)[1]

    def minimax(self, starting_state: Node, depth=10) -> Tuple[float, Union[Action, None]]:
        if starting_state.state.game_over:
            # print('game over state eval')
            return (24 if starting_state.state.whoWon() == self.color else -24), None

        if starting_state.depth >= depth:
            # return starting_state.value(), None
            return self.eval_fn(starting_state.state.board, self.color), None

        if starting_state.state.turn == self.color:
            # print('running max')
            return self.run_max(starting_state)
        else:
            # print('running min')
            return self.run_min(starting_state)

    def run_max(self, state: Node) -> Tuple[float, Union[Action, None]]:
        max_value = float('-inf')
        max_action = None

        for action in state.next_actions():
            new_game_state = state.next_node(action)
            value, _ = self.minimax(new_game_state, self.depth_limit)
            # print(f'MAX: Considering ({action.from_x}, {action.from_y}) => ({action.to_x}, {action.to_y}) '
            #       f'with value {value}')
            if value > max_value:
                max_value = value
                max_action = action
            elif value == max_value and bool(random.randint(0, 1)):
                max_value = value
                max_action = action

        if max_action is None:  # if you can't take any actions, your value is 0
            return 0, None
        return max_value, max_action

    def run_min(self, state: Node) -> Tuple[float, Union[Action, None]]:
        min_value = float('inf')
        min_action = None

        for action in state.next_actions():
            new_game_state = state.next_node(action)
            value, _ = self.minimax(new_game_state, self.depth_limit)
            # print(f'MIN: Considering ({action.from_x}, {action.from_y}) => ({action.to_x}, {action.to_y}) '
                  # f'with value {value}')
            if value < min_value:
                min_value = value
                min_action = action
            elif value == min_value and bool(random.randint(0, 1)):
                min_value = value
                min_action = action
        if min_action is None:  # if you can't take any actions, your value is 0
            return 0, None
        return min_value, min_action

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
