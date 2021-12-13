from __future__ import annotations

from checkers import Board, PlayerColor, RED


# from game_state import PlayerColor


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


def piece2val_inv(board: Board, color: PlayerColor):
    badness = 0
    for i in range(8):
        for j in range(8):
            occupant = board.location(i, j).occupant
            if occupant is not None:
                if occupant.color == color:
                    badness -= 1
                else:
                    badness += 1

    return 24 - badness


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