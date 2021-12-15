import json
import math

from matplotlib import pyplot as plt

FILENAME = "competitions/competition_(minimax.3.piece2val)_vs_(minimax_ab.3.piece2val).json"


def nodes_explored_by_move(agent_name, agent_depth, avg_explored_nodes, max_y: int):
    plt.bar(range(len(avg_explored_nodes)), height=avg_explored_nodes)
    plt.axhline(y=sum(avg_explored_nodes) / len(avg_explored_nodes), color='r', linestyle='--')
    plt.yticks(range(0, max_y, 50))
    plt.title(f'{agent_name} agent @ depth {agent_depth}: nodes explored at move #')
    plt.xlabel('Move number')
    plt.ylabel('Average nodes explored')
    plt.savefig(f'{agent_name}_agent_depth_{agent_depth}.png')
    plt.show()


def main(filename: str):
    f = open(filename)
    j = json.load(f)
    avg_red_explored_nodes = j['avg_red_explored_nodes']
    avg_blue_explored_nodes = j['avg_blue_explored_nodes']

    red_agent_name = j['red']['agent']
    red_agent_depth = j['red']['depth']

    blue_agent_name = j['blue']['agent']
    blue_agent_depth = j['blue']['depth']

    max_y = int((math.ceil(max(max(avg_red_explored_nodes), max(avg_blue_explored_nodes)) / 100) * 100) + 1)

    nodes_explored_by_move(agent_name=red_agent_name, agent_depth=red_agent_depth,
                           avg_explored_nodes=avg_red_explored_nodes, max_y=max_y)
    nodes_explored_by_move(agent_name=blue_agent_name, agent_depth=blue_agent_depth,
                           avg_explored_nodes=avg_blue_explored_nodes, max_y=max_y)


if __name__ == '__main__':
    main(FILENAME)
