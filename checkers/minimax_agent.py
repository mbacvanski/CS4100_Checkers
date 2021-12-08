import random
from typing import Tuple, Union

from checkers import Board, Game
from game_state import Action, GameState, PlayerColor, _next_player_color, piece2val


class MinimaxAgent:
    color: PlayerColor = None  # which color does this agent play for
    game: Game = None
    depth_limit: int = 0

    def __init__(self, color: PlayerColor, game: Game, depth: int):
        self.color = color
        self.game = game
        self.depth_limit = depth
        self.adversary_color = _next_player_color(self.color)

    def make_move(self, board: Board):
        move = self._get_move(board, start_from=self.game.last_hop_to)
        if move is not None:
            print(f'decided on move ({move.from_x}, {move.from_y}) => ({move.to_x}, {move.to_y})')
            self._action(current_pos=(move.from_x, move.from_y), final_pos=(move.to_x, move.to_y), board=board)
        else:
            print('no moves found ...')
            self.game.end_turn()

    def _get_move(self, board: Board, start_from=None):
        starting_state = GameState(
            board=board,
            game=self.game,
            color=self.color,
            eval_fn=piece2val,
            start_from=start_from,
        )
        return self.minimax(starting_state=starting_state, depth=self.depth_limit)[1]

    def minimax(self, starting_state: GameState, depth=10) -> Tuple[float, Union[Action, None]]:
        if starting_state.is_terminal():
            return (-1 if starting_state.current_player_color == self.color else 1), None

        if starting_state.depth > depth:
            # return self.evaluation_function(starting_state), None
            return starting_state.value(), None

        if starting_state.current_player_color == self.color:
            # print(f'running max on depth, {starting_state.depth}')
            return self.run_max(starting_state)
        else:
            # print(f'running min on depth, {starting_state.depth}')
            return self.run_min(starting_state)

    def run_max(self, state: GameState) -> Tuple[float, Union[Action, None]]:
        max_value = float('-inf')
        max_action = None

        for action in state.next_actions():
            new_game_state = state.next_state(action)
            value, _ = self.minimax(new_game_state, self.depth_limit)
            if value > max_value:
                max_value = value
                max_action = action
            elif value == max_value and bool(random.randint(0, 1)):
                max_value = value
                max_action = action

        return max_value, max_action

    def run_min(self, state: GameState) -> Tuple[float, Union[Action, None]]:
        min_value = float('inf')
        min_action = None

        for action in state.next_actions():
            new_game_state = state.next_state(action)
            value, _ = self.minimax(new_game_state, self.depth_limit)
            if value < min_value:
                min_value = value
                min_action = action
            elif value == min_value and bool(random.randint(0, 1)):
                min_value = value
                min_action = action

        return min_value, min_action

    def _action(self, current_pos, final_pos, board):
        if current_pos is None:
            self.game.end_turn()
            # board.repr_matrix()
            # print(self._generate_all_possible_moves(board))
        # print(current_pos, final_pos, board.location(current_pos[0], current_pos[1]).occupant)
        # if self.game.hop == False:
        #     if board.location(final_pos[0], final_pos[1]).occupant != None and board.location(final_pos[0], final_pos[
        #         1]).occupant.color == self.game.turn:
        #         current_pos = final_pos
        #
        #     elif current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):
        #         board.move_piece(
        #             current_pos[0], current_pos[1], final_pos[0], final_pos[1])
        #
        #         if final_pos not in board.adjacent(current_pos[0], current_pos[1]):
        #             board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
        #                                2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)
        #
        #             self.game.hop = True
        #             self.game.last_hop_to = final_pos
        #
        # if self.game.hop == True:
        #     if current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1], self.game.hop):
        #         board.move_piece(
        #             current_pos[0], current_pos[1], final_pos[0], final_pos[1])
        #         board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
        #                            2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)
        #
        #     if board.legal_moves(final_pos[0], final_pos[1], self.game.hop) == []:
        #         self.game.end_turn()
        #     else:
        #         current_pos = final_pos
        #         final_pos = board.legal_moves(
        #             current_pos[0], current_pos[1], True)
        #         if final_pos != []:
        #             print('what is going on')
        #             self._action(current_pos, final_pos[0], board)
        #         self.game.end_turn()
        # if not self.game.hop:
        #     # self.game.turn = _next_player_color(self.game.turn)
        #     self.game.turn = self.adversary_color

        # =================

        if board.location(final_pos[0], final_pos[1]).occupant != None and board.location(final_pos[0], final_pos[
            1]).occupant.color == self.game.turn:
            current_pos = final_pos

        elif current_pos is not None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):
            board.move_piece(
                current_pos[0], current_pos[1], final_pos[0], final_pos[1])

            if final_pos not in board.adjacent(current_pos[0], current_pos[1]):
                board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                   2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

                self.game.hop = True
                self.game.last_hop_to = final_pos
            else:  # not a hop
                self.game.end_turn()
                # self.game.turn = self.adversary_color
