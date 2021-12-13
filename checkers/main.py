from typing import Callable, Tuple

import checkers
from agents.minimax_agent import MinimaxAgent
##COLORS##
#             R    G    B
from eval_fns import piece2val

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
HIGH = (160, 190, 255)

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

AGENT_RED_SETUP = {
    'agent': 'Minimax',
    'color': checkers.RED,
    'depth': 2,
    'eval_fn': piece2val
}


def build_agent(game: checkers.Game, agent: str, color: Tuple, depth: int, eval_fn: Callable):
    if agent == 'Minimax':
        return MinimaxAgent(color=color, game=game, depth=depth, eval_fn=eval_fn)


def main():
    while True:
        game = checkers.Game(loop_mode=False)
        game.setup()
        agent = build_agent(game=game, **AGENT_RED_SETUP)

        while True:  # main game loop
            if game.state.turn == BLUE:
                # TO start player's turn uncomment the below line and comment a couple  of line below than that
                game.player_turn()
            else:
                print('=======================================')
                agent.make_move()

            if game.state.game_over:
                break
            game.update()


if __name__ == "__main__":
    main()
    pass
