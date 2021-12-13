from collections import Callable
from typing import Tuple

import checkers
from agents.agent import Agent
from agents.minimax_agent import MinimaxAgent
from agents.random_agent import RandomAgent


def build_agent(game: checkers.Game, agent: str, color: Tuple, depth: int = None, eval_fn: Callable = None) -> Agent:
    if agent == 'minimax':
        return MinimaxAgent(color=color, game=game, depth=depth, eval_fn=eval_fn)
    elif agent == 'random':
        return RandomAgent(color=color, game=game, eval_fn=None)
