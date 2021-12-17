from __future__ import annotations

import random

from checkers import *
from checkers import Action, PlayerColor
from eval_fns import _dists_to_all_pieces, furthest_king, piece2val, piece2val_move_to_opponent

MovesForPiece = namedtuple("MovesForPiece", "x y actions")


class Node:
    state: GameState = None
    depth: int = 0
    eval_fn = piece2val
    start_from: Tuple = None

    def __init__(self, state: GameState, depth: int = 0, eval_fn=piece2val, start_from: Tuple = None):
        self.state = state
        self.depth = depth
        self.eval_fn = eval_fn
        self.start_from = start_from

    def is_terminal(self) -> bool:
        return self.state.whoWon() is not None

    def next_actions(self) -> List[Action]:
        if self.start_from is not None:
            i, j = self.start_from
            moves = [MovesForPiece(i, j, self.state.board.legal_moves(i, j, self.state.mid_hop))]
        else:
            moves = self._generate_moves()

        actions: List[Action] = []
        for move_from_x, move_from_y, move_tos in moves:
            for move_to in move_tos:
                actions.append(Action(move_from_x, move_from_y, move_to[0], move_to[1]))

        return actions

    # Successor function returns a new GameState object
    def next_node(self, action: Action) -> Node:
        next_state = deepcopy(self.state)
        self._apply_action_to_state(state=next_state, action=action)

        next_state = Node(
            state=next_state,
            depth=self.depth + 1,
            eval_fn=self.eval_fn
        )
        return next_state

    def value(self) -> float:
        return self.eval_fn(self.state.board, self.state.turn)

    def _generate_moves(self) -> List[MovesForPiece]:
        for i in range(8):
            for j in range(8):
                if (self.state.board.legal_moves(i, j, self.state.mid_hop) != []
                        and self.state.board.location(i, j).occupant is not None
                        and self.state.board.location(i, j).occupant.color == self.state.turn):
                    yield MovesForPiece(i, j, self.state.board.legal_moves(i, j, self.state.mid_hop))

    def _apply_action_to_state(self, state: GameState, action: Action):
        current_pos, final_pos = (action.from_x, action.from_y), (action.to_x, action.to_y)

        if (state.board.location(final_pos[0], final_pos[1]).occupant is not None
                and state.board.location(final_pos[0], final_pos[1]).occupant.color == self.state.turn):
            state.end_turn()
            return

        state.board.move_piece(current_pos[0], current_pos[1], final_pos[0], final_pos[1])
        if final_pos not in state.board.adjacent(current_pos[0], current_pos[1]):  # hop
            state.board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) // 2,
                                     current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

            if state.board.legal_moves(final_pos[0], final_pos[1], mid_hop=True):
                # More legal moves to make, we are mid-hop
                state.mid_hop = True
            else:
                # No more legal moves now
                state.end_turn()
        else:
            state.end_turn()


def _break_ties_distance(curr_best_action: Action, new_action: Action, node: Node, color: PlayerColor):
    curr_best_board = node.next_node(curr_best_action).state.board
    new_board = node.next_node(new_action).state.board

    max_value = piece2val_move_to_opponent(curr_best_board, color)
    current_value = piece2val_move_to_opponent(new_board, color)

    # if the two actions are of equal value, choose one randomly
    if current_value == max_value:
        return bool(random.randint(0, 1))

    # otherwise, return the action that leads to the centers of mass being closer
    return current_value > max_value


def _break_ties_by_king_dist(curr_best_action: Action, new_action: Action, node: Node, color: PlayerColor):
    curr_best_board = node.next_node(curr_best_action).state.board
    new_board = node.next_node(new_action).state.board

    max_value = furthest_king(curr_best_board, color)
    current_value = furthest_king(new_board, color)

    # if the two actions are of equal value, choose one randomly
    if current_value == max_value:
        return bool(random.randint(0, 1))

    # otherwise, return the action that leads to the centers of mass being closer
    print(f'breaking tie by king dist: max_value={max_value} vs {current_value}')
    return current_value < max_value


def _break_ties_by_all_dists(curr_best_action: Action, new_action: Action, node: Node, color: PlayerColor):
    curr_best_board = node.next_node(curr_best_action).state.board
    new_board = node.next_node(new_action).state.board

    max_value = _dists_to_all_pieces(curr_best_board)
    current_value = _dists_to_all_pieces(new_board)

    # if the two actions are of equal value, choose one randomly
    if current_value == max_value:
        return bool(random.randint(0, 1))

    # otherwise, return the action that leads to the centers of mass being closer
    # print(f'breaking tie by all dists: max_value={max_value} vs {current_value}')
    return current_value < max_value
