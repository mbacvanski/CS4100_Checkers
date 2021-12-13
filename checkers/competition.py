import json
import multiprocessing
import multiprocessing as mp
import os
from typing import Callable, Dict, Tuple

import checkers
from eval_fns import piece2val, piece2val_favor_kings, piece2val_keep_back_row
from minimax_agent import MinimaxAgent
from minimax_agent_2 import MinimaxAgent as MinimaxAgent_2

NUM_GAMES = 50
MAX_MOVES = 100


def agent_str(agent: Dict) -> str:
    return f'({agent.get("agent")}.{agent.get("depth")}.{agent.get("eval_fn").__name__})'


AGENT_RED_SETUP = {
    'agent': 'Minimax',
    'color': checkers.RED,
    'depth': 1,
    'eval_fn': piece2val
}

AGENT_BLUE_SETUP = {
    'agent': 'Minimax',
    'color': checkers.BLUE,
    'depth': 2,
    'eval_fn': piece2val
}


def build_agent(game: checkers.Game, agent: str, color: Tuple, depth: int, eval_fn: Callable):
    if agent == 'Minimax':
        return MinimaxAgent(color=color, game=game, depth=depth, eval_fn=eval_fn)
    if agent == 'Minimax_2':
        return MinimaxAgent_2(color=color, game=game, depth=depth, eval_fn=eval_fn)


def run_game_once(x):
    """
    Returns TRUE if red wins, FALSE if blue wins
    """
    game = checkers.Game(loop_mode=True)
    game.setup()
    # agent_blue = MinimaxAgent(color=checkers.BLUE, game=game, depth=2, eval_fn=piece2val)
    # agent_red = MinimaxAgent(color=checkers.RED, game=game, depth=1, eval_fn=piece2val_favor_kings)
    agent_blue = build_agent(**{'game': game, **AGENT_BLUE_SETUP})
    agent_red = build_agent(**{'game': game, **AGENT_RED_SETUP})
    print(f'⏳ Starting run {x}...')

    while True and game.state.move_count < MAX_MOVES:  # main game loop
        if game.state.turn == checkers.BLUE:
            agent_blue.make_move()
        else:
            agent_red.make_move()
        if game.state.game_over:
            return game.state.whoWon()

        game.update()

    return None


def parallel_main():
    print('Agent Red: ' + str(AGENT_RED_SETUP))
    print('Agent Blue: ' + str(AGENT_BLUE_SETUP))

    pool = mp.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(run_game_once, range(NUM_GAMES))
    print(results)

    red_wins = sum([1 for x in results if x == checkers.RED])
    blue_wins = sum([1 for x in results if x == checkers.BLUE])
    draws = sum([1 for x in results if x is None])

    red_win_rate = red_wins / len(results)
    blue_win_rate = blue_wins / len(results)

    print(f'Red wins {red_wins} / {len(results)} = {red_win_rate * 100}%')
    print(f'Blue wins {blue_wins} / {len(results)} = {blue_win_rate * 100}%')
    print(f'Draws = {draws}')

    file_contents = {
        'red': AGENT_RED_SETUP,
        'blue': AGENT_BLUE_SETUP,
        'num_games': NUM_GAMES,
        'red_wins': red_wins,
        'blue_wins': blue_wins,
        'draws': draws,
        'draw_threshold': MAX_MOVES,
        'red_win_rate': red_win_rate,
        'blue_win_rate': blue_win_rate,
    }

    filename = f'results/competitions/competition_{agent_str(AGENT_RED_SETUP)}_vs_{agent_str(AGENT_BLUE_SETUP)}.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as fp:
        json.dump(file_contents, fp, indent=2, default=lambda o: o.__name__)


if __name__ == '__main__':
    # main()
    parallel_main()
