import json
import math

from matplotlib import pyplot as plt

FILENAME = "competitions/competition_(minimax_ab.4.piece2val)_vs_(random.None.).json"


def compare_nodes_explored_by_move(a_name, a_depth, a_explored, b_name, b_depth, b_explored):
    plt.bar(range(len(a_explored)), height=a_explored, color='b', label=f'{a_name} @ depth {a_depth}', alpha=0.5)
    plt.bar(range(len(b_explored)), height=b_explored, color='r', label=f'{b_name} @ depth {b_depth}', alpha=0.5)
    max_y = int(max(max(a_explored), max(b_explored)))
    plt.yticks(range(0, max_y + 1, int(max_y // 20)))
    plt.xlabel('Move number')
    plt.ylabel('Average nodes explored')
    plt.legend()
    plt.savefig(f'{a_name}_depth_{a_depth}_vs_{b_name}_depth_{b_depth}')
    plt.show()


def compare_three_nodes_explored_by_move(a_name, a_depth, a_explored,
                                         b_name, b_depth, b_explored,
                                         c_name, c_depth, c_explored):
    plt.bar(range(len(a_explored)), height=a_explored, color='b', label=f'{a_name} @ depth {a_depth}', alpha=0.4)
    plt.bar(range(len(b_explored)), height=b_explored, color='r', label=f'{b_name} @ depth {b_depth}', alpha=0.4)
    plt.bar(range(len(c_explored)), height=c_explored, color='g', label=f'{c_name} @ depth {c_depth}', alpha=0.4)
    max_y = int(max(max(a_explored), max(b_explored), max(c_explored)))
    plt.yticks(range(0, max_y + 1, int(max_y // 20)))
    plt.xlabel('Move number')
    plt.ylabel('Average nodes explored')
    plt.legend()
    plt.savefig(f'{a_name}_depth_{a_depth}_vs_{b_name}_depth_{b_depth}_vs_{c_name}_depth_{c_depth}')
    plt.show()


def nodes_explored_by_move(agent_name, agent_depth, avg_explored_nodes, max_y: int):
    plt.bar(range(len(avg_explored_nodes)), height=avg_explored_nodes)
    plt.axhline(y=sum(avg_explored_nodes) / len(avg_explored_nodes), color='r', linestyle='--')
    # plt.yticks(range(0, max_y, 200))
    plt.yticks(range(0, 5401, 200))
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
    red_agent_depth = j['red'].get('depth', '')

    blue_agent_name = j['blue']['agent']
    blue_agent_depth = j['blue'].get('depth', '')

    max_y = int((math.ceil(max(max(avg_red_explored_nodes), max(avg_blue_explored_nodes)) / 100) * 100) + 1)

    nodes_explored_by_move(agent_name=red_agent_name, agent_depth=red_agent_depth,
                           avg_explored_nodes=avg_red_explored_nodes, max_y=max_y)
    nodes_explored_by_move(agent_name=blue_agent_name, agent_depth=blue_agent_depth,
                           avg_explored_nodes=avg_blue_explored_nodes, max_y=max_y)


def compare_alpha_beta_4():
    minimax_ab = open('competitions/competition_(minimax_ab.4.piece2val)_vs_(random.None.).json')
    minimax = open('competitions/competition_(minimax.4.piece2val)_vs_(random.None.).json')
    j_minimax_ab = json.load(minimax_ab)
    j_minimax = json.load(minimax)

    avg_minimax_ab_explored_nodes = j_minimax_ab['avg_red_explored_nodes']
    avg_minimax_explored_nodes = j_minimax['avg_red_explored_nodes']

    minimax_ab_agent_name = j_minimax_ab['red']['agent']
    minimax_ab_agent_depth = j_minimax_ab['red'].get('depth', '')

    minimax_agent_name = j_minimax['red']['agent']
    minimax_agent_depth = j_minimax['red'].get('depth', '')

    compare_nodes_explored_by_move(a_name=minimax_ab_agent_name, a_depth=minimax_ab_agent_depth,
                                   a_explored=avg_minimax_ab_explored_nodes, b_name=minimax_agent_name,
                                   b_depth=minimax_agent_depth, b_explored=avg_minimax_explored_nodes)


def compare_alpha_beta_random_vs_jumps():
    rando = open('competitions/competition_(minimax_ab_random.4.piece2val)_vs_(random.None.).json')
    jumps = open('competitions/competition_(minimax_ab_jumps_first.4.piece2val)_vs_(random.None.).json')
    j_rando = json.load(rando)
    j_jumps = json.load(jumps)

    avg_rando_explored_nodes = j_rando['avg_red_explored_nodes']
    avg_jumps_explored_nodes = j_jumps['avg_red_explored_nodes']

    rando_agent_name = j_rando['red']['agent']
    rando_agent_depth = j_rando['red'].get('depth', '')

    jumps_agent_name = j_jumps['red']['agent']
    jumps_agent_depth = j_jumps['red'].get('depth', '')

    compare_nodes_explored_by_move(a_name=rando_agent_name, a_depth=rando_agent_depth,
                                   a_explored=avg_rando_explored_nodes, b_name=jumps_agent_name,
                                   b_depth=jumps_agent_depth, b_explored=avg_jumps_explored_nodes)


def compare_alpha_beta_default_vs_random():
    rando = open('competitions/competition_(minimax_ab_random.4.piece2val)_vs_(random.None.).json')
    default = open('competitions/competition_(minimax.4.piece2val)_vs_(random.None.).json')
    j_rando = json.load(rando)
    j_default = json.load(default)

    avg_rando_explored_nodes = j_rando['avg_red_explored_nodes']
    avg_default_explored_nodes = j_default['avg_red_explored_nodes']

    rando_agent_name = j_rando['red']['agent']
    rando_agent_depth = j_rando['red'].get('depth', '')

    default_agent_name = j_default['red']['agent']
    default_agent_depth = j_default['red'].get('depth', '')

    compare_nodes_explored_by_move(a_name=rando_agent_name, a_depth=rando_agent_depth,
                                   a_explored=avg_rando_explored_nodes, b_name=default_agent_name,
                                   b_depth=default_agent_depth, b_explored=avg_default_explored_nodes)


def compare_all_ab():
    rando = open('competitions/competition_(minimax_ab_random.4.piece2val)_vs_(random.None.).json')
    default = open('competitions/competition_(minimax.4.piece2val)_vs_(random.None.).json')
    jumps = open('competitions/competition_(minimax_ab_jumps_first.4.piece2val)_vs_(random.None.).json')
    j_rando = json.load(rando)
    j_default = json.load(default)
    j_jumps = json.load(jumps)

    avg_rando_explored_nodes = j_rando['avg_red_explored_nodes']
    avg_default_explored_nodes = j_default['avg_red_explored_nodes']
    avg_jumps_explored_nodes = j_jumps['avg_red_explored_nodes']

    rando_agent_name = j_rando['red']['agent']
    default_agent_name = j_default['red']['agent']
    jumps_agent_name = j_jumps['red']['agent']

    rando_agent_depth = j_rando['red'].get('depth', '')
    default_agent_depth = j_default['red'].get('depth', '')
    jumps_agent_depth = j_jumps['red'].get('depth', '')

    compare_three_nodes_explored_by_move(a_name=rando_agent_name,
                                         a_depth=rando_agent_depth,
                                         a_explored=avg_rando_explored_nodes,
                                         b_name=default_agent_name,
                                         b_depth=default_agent_depth,
                                         b_explored=avg_default_explored_nodes,
                                         c_name=jumps_agent_name,
                                         c_depth=jumps_agent_depth,
                                         c_explored=avg_jumps_explored_nodes)


if __name__ == '__main__':
    # main(FILENAME)
    # compare_alpha_beta_4()
    # compare_alpha_beta_random_vs_jumps()
    # compare_alpha_beta_default_vs_random()
    compare_all_ab()
