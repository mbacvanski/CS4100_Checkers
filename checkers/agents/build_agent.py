from collections import Callable
from typing import Tuple

import checkers
from agents.agent import Agent
from agents.minimax_agent import MinimaxAgent
from agents.minimax_alpha_beta_agent import MinimaxAlphaBetaAgent
from agents.minimax_alpha_beta_jumps_first_agent import MinimaxAlphaBetaJumpsFirstAgent
from agents.minimax_alpha_beta_random_ordering_agent import MinimaxAlphaBetaRandomAgent
from agents.random_agent import RandomAgent


def build_agent(game: checkers.Game, agent: str, color: Tuple, depth: int = None, eval_fn: Callable = None,
                tiebreaker_fn: Callable = None) -> Agent:
    if agent == 'minimax':
        return MinimaxAgent(color=color, game=game, depth=depth, eval_fn=eval_fn)
    elif agent == 'minimax_ab':
        return MinimaxAlphaBetaAgent(color=color, game=game, depth=depth, eval_fn=eval_fn)
    elif agent == 'minimax_ab_random':
        return MinimaxAlphaBetaRandomAgent(color=color, game=game, depth=depth, eval_fn=eval_fn)
    elif agent == 'minimax_ab_jumps_first':
        return MinimaxAlphaBetaJumpsFirstAgent(color=color, game=game, depth=depth, eval_fn=eval_fn,
                                               tiebreaker_fn=tiebreaker_fn)
    elif agent == 'random':
        return RandomAgent(color=color, game=game, eval_fn=None)
