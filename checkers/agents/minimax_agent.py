import random
from typing import Tuple, Union

from agents.build_agent import Agent
from checkers import Game, Action
from eval_fns import piece2val
from game_state import Node, PlayerColor


class MinimaxAgent(Agent):
    depth_limit: int = 0

    def __init__(self, color: PlayerColor, game: Game, depth: int, eval_fn=piece2val):
        super().__init__(color, game, eval_fn)
        self.depth_limit = depth

    def _get_move(self, start_from: Tuple = None) -> Tuple[Action, int]:
        starting_state = Node(
            state=self.game.state,
            eval_fn=self.eval_fn,
            start_from=start_from,
        )
        value, action, nodes_explored = self.minimax(starting_state=starting_state, depth=self.depth_limit)
        return action, nodes_explored

    def minimax(self, starting_state: Node, depth=10) -> Tuple[float, Union[Action, None], int]:
        if starting_state.state.game_over:
            # print('game over state eval')
            return (24 if starting_state.state.whoWon() == self.color else -24), None, 0

        if starting_state.depth >= depth:
            # return starting_state.value(), None
            return self.eval_fn(starting_state.state.board, self.color), None, 0

        if starting_state.state.turn == self.color:
            # print('running max')
            return self.run_max(starting_state)
        else:
            # print('running min')
            return self.run_min(starting_state)

    def run_max(self, state: Node) -> Tuple[float, Union[Action, None], int]:
        max_value = float('-inf')
        max_action = None

        nodes_explored = 0
        for action in state.next_actions():
            new_game_state = state.next_node(action)
            nodes_explored += 1
            value, _, explored = self.minimax(new_game_state, self.depth_limit)
            nodes_explored += explored
            # print(f'MAX: Considering ({action.from_x}, {action.from_y}) => ({action.to_x}, {action.to_y}) '
            #       f'with value {value}')
            if value > max_value:
                max_value = value
                max_action = action
            elif value == max_value and bool(random.randint(0, 1)):
                max_value = value
                max_action = action

        if max_action is None:  # if you can't take any actions, your value is 0
            return 0, None, nodes_explored
        return max_value, max_action, nodes_explored

    def run_min(self, state: Node) -> Tuple[float, Union[Action, None], int]:
        min_value = float('inf')
        min_action = None

        nodes_explored = 0
        for action in state.next_actions():
            new_game_state = state.next_node(action)
            nodes_explored += 1
            value, _, explored = self.minimax(new_game_state, self.depth_limit)
            nodes_explored += explored
            # print(f'MIN: Considering ({action.from_x}, {action.from_y}) => ({action.to_x}, {action.to_y}) '
            # f'with value {value}')
            if value < min_value:
                min_value = value
                min_action = action
            elif value == min_value and bool(random.randint(0, 1)):
                min_value = value
                min_action = action
        if min_action is None:  # if you can't take any actions, your value is 0
            return 0, None, nodes_explored
        return min_value, min_action, nodes_explored
