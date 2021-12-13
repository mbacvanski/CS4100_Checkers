from abc import ABC, abstractmethod

from checkers import BLUE, Game, PlayerColor, RED


class Agent(ABC):
    color: PlayerColor = None  # which color does this agent play for
    game: Game = None

    def __init__(self, color: PlayerColor, game: Game, eval_fn):
        self.color = color
        self.game = game
        self.adversary_color = _next_player_color(self.color)
        self.eval_fn = eval_fn

    @abstractmethod
    def make_move(self):
        pass


def _next_player_color(color: PlayerColor) -> PlayerColor:
    if color == BLUE:
        return RED
    elif color == RED:
        return BLUE
