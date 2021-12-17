from typing import Tuple

from agents.minimax_alpha_beta_jumps_first_agent import MinimaxAlphaBetaJumpsFirstAgent
from checkers import Action, _next_player_color
from game_state import Node


class MinimaxAlphaBetaJumpsFirstVariableDepthAgent(MinimaxAlphaBetaJumpsFirstAgent):
    def _get_move(self, start_from: Tuple = None) -> Tuple[Action, int]:
        starting_state = Node(
            state=self.game.state,
            eval_fn=self.eval_fn,
            start_from=start_from,
        )
        min_players_left = min(len(starting_state.state.board.get_locations_by_color(self.color)),
                               len(starting_state.state.board.get_locations_by_color(_next_player_color(self.color))))
        depth = max(self.depth_limit, 12 - min_players_left)
        print(f'Searching depth {depth}')
        value, action, nodes_explored = self.minimax(starting_state=starting_state, depth=depth)
        return action, nodes_explored
