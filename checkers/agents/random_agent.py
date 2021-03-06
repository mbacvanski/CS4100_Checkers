import random
from typing import Tuple

from agents.agent import Agent
from game_state import Node
from checkers import Action


class RandomAgent(Agent):

    def _get_move(self, start_from: Tuple = None) -> Tuple[Action, int]:
        starting_state = Node(
            state=self.game.state,
            eval_fn=self.eval_fn,
            start_from=start_from,
        )
        actions = starting_state.next_actions()
        return random.choice(actions), 0
