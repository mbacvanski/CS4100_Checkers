import json
import multiprocessing
import multiprocessing as mp
import os
from typing import Dict

import checkers
from agents.build_agent import build_agent
from eval_fns import piece2val

NUM_GAMES = 50
MAX_MOVES = 150


def agent_str(agent: Dict) -> str:
    return f'({agent.get("agent")}.{agent.get("depth")}.{agent.get("eval_fn").__name__ if "eval_fn" in agent else ""})'


AGENT_RED_SETUP = {
    'agent': 'minimax',
    'color': checkers.RED,
    'depth': 3,
    'eval_fn': piece2val
}

AGENT_BLUE_SETUP = {
    'agent': 'random',
    'color': checkers.BLUE,
}


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
