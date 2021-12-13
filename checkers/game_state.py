from __future__ import annotations

from collections import namedtuple
from typing import List

from checkers import *
from eval_fns import piece2val

MovesForPiece = namedtuple("MovesForPiece", "x y actions")
Action = namedtuple("Action", "from_x from_y to_x to_y")


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
