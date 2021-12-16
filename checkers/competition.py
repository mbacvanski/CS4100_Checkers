import itertools
import json
import multiprocessing
import multiprocessing as mp
import os
from typing import Any, Dict, List, Tuple

import checkers
from agents.build_agent import build_agent
from eval_fns import piece2val, piece2val_move_to_opponent

NUM_GAMES = 20
MAX_MOVES = 150


def agent_str(agent: Dict) -> str:
    return f'({agent.get("agent")}.{agent.get("depth")}.{agent.get("eval_fn").__name__ if "eval_fn" in agent else ""})'


AGENT_RED_SETUP = {
    'agent': 'minimax_ab',
    'color': checkers.RED,
    'depth': 3,
    'eval_fn': piece2val_move_to_opponent
}

AGENT_BLUE_SETUP = {
    'agent': 'minimax_ab',
    'color': checkers.BLUE,
    'depth': 3,
    'eval_fn': piece2val
}


# AGENT_BLUE_SETUP = {
#     'agent': 'minimax_ab',
#     'color': checkers.BLUE,
#     'depth': 4,
#     'eval_fn': piece2val
# }


def run_game_once(x) -> Tuple[Any, List[int]]:
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

    nodes_explored_counts = [0]

    last_turn = game.state.turn
    while True and game.state.move_count < MAX_MOVES:  # main game loop
        same_color = False
        if game.state.turn == last_turn:
            same_color = True
        last_turn = game.state.turn

        if game.state.turn == checkers.BLUE:
            nodes_explored = agent_blue.make_move()
        else:
            nodes_explored = agent_red.make_move()

        if same_color:
            nodes_explored_counts[-1] += nodes_explored
        else:
            nodes_explored_counts.append(nodes_explored)

        if game.state.game_over:
            return game.state.whoWon(), nodes_explored_counts

        game.update()

    return None, nodes_explored_counts


def parallel_main():
    print('Agent Red: ' + str(AGENT_RED_SETUP))
    print('Agent Blue: ' + str(AGENT_BLUE_SETUP))

    pool = mp.Pool(processes=multiprocessing.cpu_count())
    results = pool.map(run_game_once, range(NUM_GAMES))
    print(results)

    red_wins = 0
    blue_wins = 0
    draws = 0
    blue_explored_nodes = []
    red_explored_nodes = []

    for i in range(NUM_GAMES):
        who_won = results[i][0]
        nodes_explored_list = results[i][1]
        blue_explored_here = [x for idx, x in enumerate(nodes_explored_list) if idx % 2 == 0]  # blue goes first
        red_explored_here = [x for idx, x in enumerate(nodes_explored_list) if idx % 2 == 1]

        blue_explored_nodes = [sum(x) for x in
                               itertools.zip_longest(blue_explored_nodes, blue_explored_here, fillvalue=0)]
        red_explored_nodes = [sum(x)
                              for x in itertools.zip_longest(red_explored_nodes, red_explored_here, fillvalue=0)]

        if who_won == checkers.RED:
            red_wins += 1
        elif who_won == checkers.BLUE:
            blue_wins += 1
        else:
            draws += 1

    avg_red_explored_nodes = [x / NUM_GAMES for x in red_explored_nodes]
    avg_blue_explored_nodes = [x / NUM_GAMES for x in blue_explored_nodes]

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
        'avg_red_explored_nodes': avg_red_explored_nodes,
        'avg_blue_explored_nodes': avg_blue_explored_nodes,
    }

    filename = f'results/competitions/competition_{agent_str(AGENT_RED_SETUP)}_vs_{agent_str(AGENT_BLUE_SETUP)}.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as fp:
        json.dump(file_contents, fp, indent=2, default=lambda o: o.__name__)


if __name__ == '__main__':
    parallel_main()
