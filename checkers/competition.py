import multiprocessing as mp

import checkers
from game_state import piece2val, piece2val_favor_kings
from minimax_agent import MinimaxAgent


def run_game_once(x):
    """
    Returns TRUE if red wins, FALSE if blue wins
    """
    game = checkers.Game(loop_mode=True)
    game.setup()
    agent_blue = MinimaxAgent(color=checkers.BLUE, game=game, depth=1, eval_fn=piece2val)
    agent_red = MinimaxAgent(color=checkers.RED, game=game, depth=1, eval_fn=piece2val_favor_kings)

    while True:  # main game loop
        if game.turn == checkers.BLUE:
            agent_blue.make_move(board=game.board)
        else:
            agent_red.make_move(board=game.board)

        if game.endit:
            print('END GAME ====================')
            if game.turn == checkers.RED:
                return True
            else:
                return False

        game.update()


def parallel_main():
    NUM_GAMES = 50

    pool = mp.Pool(processes=8)
    results = pool.map(run_game_once, range(NUM_GAMES))
    print(results)
    print(f'Red wins {sum(results)} / {len(results)} = {sum(results) / len(results)}%')


if __name__ == '__main__':
    # main()
    parallel_main()
