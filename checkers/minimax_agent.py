from typing import Tuple, Union

from checkers import Board, Game
from game_state import Action, GameState, PlayerColor, _next_player_color


class MinimaxAgent:
    color: PlayerColor = None  # which color does this agent play for
    game: Game = None
    depth: int = 0

    def __init__(self, color: PlayerColor, game: Game, depth: int):
        self.color = color
        self.game = game
        self.depth = depth

    def make_move(self, board: Board):
        move = self._get_move(board)
        self._action(current_pos=(move.from_x, move.from_y), final_pos=(move.to_x, move.to_y), board=board)

    def _get_move(self, board: Board):
        starting_state = GameState(
            board=board,
            game=self.game,
            color=self.color
        )
        return self.minimax(starting_state=starting_state, depth=self.depth)[1]

    def minimax(self, starting_state: GameState, depth=100) -> Tuple[float, Union[Action, None]]:
        if starting_state.is_terminal():
            return (-1 if starting_state.current_player_color == self.color else 1), None

        # if starting_state.depth > depth:
        #     return self.evaluation_function

        if starting_state.current_player_color == self.color:
            print(f'running max on depth, {starting_state.depth}')
            return self.run_max(starting_state)
        else:
            print(f'running min on depth, {starting_state.depth}')
            return self.run_min(starting_state)

    def run_max(self, state: GameState) -> Tuple[float, Union[Action, None]]:
        max_value = float('-inf')
        max_action = None

        for action in state.next_actions():
            new_game_state = state.next_state(action)
            value, _ = self.minimax(new_game_state, self.depth)
            if value > max_value:
                max_value = value
                max_action = action

        return max_value, max_action

    def run_min(self, state: GameState) -> Tuple[float, Union[Action, None]]:
        min_value = float('inf')
        max_action = None

        for action in state.next_actions():
            new_game_state = state.next_state(action)
            value, _ = self.minimax(new_game_state, self.depth)
            if value < min_value:
                min_value = value
                max_action = action

        return min_value, max_action

    def _action(self, current_pos, final_pos, board):
        if current_pos is None:
            self.game.end_turn()
            # board.repr_matrix()
            # print(self._generate_all_possible_moves(board))
        # print(current_pos, final_pos, board.location(current_pos[0], current_pos[1]).occupant)
        if self.game.hop == False:
            if board.location(final_pos[0], final_pos[1]).occupant != None and board.location(final_pos[0], final_pos[
                1]).occupant.color == self.game.turn:
                current_pos = final_pos

            elif current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1]):
                board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])

                if final_pos not in board.adjacent(current_pos[0], current_pos[1]):
                    board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                       2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

                    self.game.hop = True
                    current_pos = final_pos
                    final_pos = board.legal_moves(
                        current_pos[0], current_pos[1], True)
                    if final_pos != []:
                        # print("HOP in Action", current_pos, final_pos)
                        self._action(current_pos, final_pos[0], board)
                    self.game.end_turn()

        if self.game.hop == True:
            if current_pos != None and final_pos in board.legal_moves(current_pos[0], current_pos[1], self.game.hop):
                board.move_piece(
                    current_pos[0], current_pos[1], final_pos[0], final_pos[1])
                board.remove_piece(current_pos[0] + (final_pos[0] - current_pos[0]) //
                                   2, current_pos[1] + (final_pos[1] - current_pos[1]) // 2)

            if board.legal_moves(final_pos[0], final_pos[1], self.game.hop) == []:
                self.game.end_turn()
            else:
                current_pos = final_pos
                final_pos = board.legal_moves(
                    current_pos[0], current_pos[1], True)
                if final_pos != []:
                    # print("HOP in Action", current_pos, final_pos)
                    self._action(current_pos, final_pos[0], board)
                self.game.end_turn()
        if self.game.hop != True:
            self.game.turn = _next_player_color(self.game.turn)
