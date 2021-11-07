from unittest import TestCase

from checkers import CheckersGameState, Location, Move, Piece, Player


class TestCheckersGameState(TestCase):
    def test_reset(self):
        game = CheckersGameState()
        self.assertEqual(game.board, [
            [None, Piece(player=Player.RED), None, Piece(player=Player.RED), None, Piece(player=Player.RED), None,
             Piece(player=Player.RED)],
            [Piece(player=Player.RED), None, Piece(player=Player.RED), None, Piece(player=Player.RED), None,
             Piece(player=Player.RED), None],
            [None, Piece(player=Player.RED), None, Piece(player=Player.RED), None, Piece(player=Player.RED), None,
             Piece(player=Player.RED)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Piece(player=Player.WHITE), None, Piece(player=Player.WHITE), None, Piece(player=Player.WHITE), None,
             Piece(player=Player.WHITE), None],
            [None, Piece(player=Player.WHITE), None, Piece(player=Player.WHITE), None, Piece(player=Player.WHITE), None,
             Piece(player=Player.WHITE)],
            [Piece(player=Player.WHITE), None, Piece(player=Player.WHITE), None, Piece(player=Player.WHITE), None,
             Piece(player=Player.WHITE), None]])

    def test_is_move_valid(self):
        game = CheckersGameState()
        self.assertTrue(game.is_move_valid(Move(start=Location(row=2, col=1), end=Location(row=3, col=0))))
        self.assertTrue(game.is_move_valid(Move(start=Location(row=2, col=1), end=Location(row=3, col=2))))
        self.assertFalse(game.is_move_valid(Move(start=Location(row=2, col=1), end=Location(row=2, col=2))))
        self.assertFalse(game.is_move_valid(Move(start=Location(row=2, col=1), end=Location(row=2, col=0))))
