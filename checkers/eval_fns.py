from __future__ import annotations

from checkers import Board, PlayerColor, RED, _next_player_color


def piece2val(board: Board, color: PlayerColor):
    score = 0
    for i in range(8):
        for j in range(8):
            occupant = board.location(i, j).occupant
            if occupant is not None:
                if occupant.color == color:
                    score += 1
                else:
                    score -= 1
    return score


def piece2val_keep_back_row(board: Board, color: PlayerColor):
    score = 0
    for i in range(8):
        for j in range(8):
            occupant = board.location(i, j).occupant
            if occupant is not None:
                if occupant.color == color:
                    score += 1
                else:
                    score -= 1

    if color == RED:
        # incentive to keep pieces in the back row to prevent opponent from becoming a king
        for i in range(0, 8, 2):
            occupant = board.location(i, 0).occupant
            if occupant is not None and occupant.color == color:
                score += occupant.value * 0.5
    else:
        for i in range(0, 8, 2):
            occupant = board.location(i, 7).occupant
            if occupant is not None and occupant.color == color:
                score += occupant.value * 0.5

    return score


def piece2val_favor_kings(board: Board, color: PlayerColor):
    score = 0
    for i in range(8):
        for j in range(8):
            occupant = board.location(i, j).occupant
            if occupant is not None:
                value = 1 if occupant.king else 5
                if occupant.color == color:
                    score += value
                else:
                    score -= value
    return score


def piece2val_move_to_opponent(board: Board, color: PlayerColor) -> int:
    self_pieces = board.get_locations_by_color(color)  # (x,y) tuples
    self_x = sum([x for x, y in self_pieces]) / len(self_pieces)
    self_y = sum([y for x, y in self_pieces]) / len(self_pieces)

    opponent_pieces = board.get_locations_by_color(_next_player_color(color))
    opponent_x = sum([x for x, y in opponent_pieces]) / len(opponent_pieces)
    opponent_y = sum([y for x, y in opponent_pieces]) / len(opponent_pieces)

    # minimum score is when centers of mass are at opposite corners, which is maximum distance
    distance = ((self_x - opponent_x) ** 2 + (self_y - opponent_y) ** 2) ** 0.5
    score = ((2 * (7 ** 2)) ** .5) - distance

    return piece2val(board=board, color=color) + score
