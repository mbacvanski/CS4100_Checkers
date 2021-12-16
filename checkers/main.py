import checkers
##COLORS##
#             R    G    B
from agents.build_agent import build_agent
from eval_fns import piece2val_move_to_opponent, piece2val
from game_state import _break_ties_distance

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
    'agent': 'minimax_ab_jumps_first',
    'color': checkers.RED,
    'depth': 3,
    'eval_fn': piece2val,
    'tiebreaker_fn': _break_ties_distance,
}


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
                nodes_explored = agent.make_move()
                print(f'Explored {nodes_explored} nodes')

            if game.state.game_over:
                break
            game.update()


if __name__ == "__main__":
    main()
    pass
