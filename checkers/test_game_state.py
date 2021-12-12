from unittest import TestCase

from checkers import BLUE, Board, GameState, Piece, RED
from game_state import Action, Node


class TestNode(TestCase):
    def test_is_terminal(self):
        state = GameState(board=Board(), turn=BLUE)
        self.assertFalse(Node(state=state).is_terminal())

    def test_next_actions_board_start(self):
        state = GameState(board=Board(), turn=BLUE)
        self.assertEqual(set(Node(state).next_actions()), {
            Action(from_x=1, from_y=5, to_x=0, to_y=4),
            Action(from_x=1, from_y=5, to_x=2, to_y=4),
            Action(from_x=3, from_y=5, to_x=2, to_y=4),
            Action(from_x=3, from_y=5, to_x=4, to_y=4),
            Action(from_x=5, from_y=5, to_x=4, to_y=4),
            Action(from_x=5, from_y=5, to_x=6, to_y=4),
            Action(from_x=7, from_y=5, to_x=6, to_y=4),
        })

    def test_double_jump(self):
        b = double_jump_board()
        state = GameState(board=b, turn=RED)
        node = Node(state)

        self.assertTrue(Action(from_x=0, from_y=0, to_x=2, to_y=2) in node.next_actions())
        node = node.next_node(Action(from_x=0, from_y=0, to_x=2, to_y=2))
        self.assertTrue(node.state.mid_hop)
        self.assertEqual(node.state.turn, RED)

        self.assertTrue(Action(from_x=2, from_y=2, to_x=4, to_y=4) in node.next_actions())
        node = node.next_node(Action(from_x=2, from_y=2, to_x=4, to_y=4))
        self.assertFalse(node.state.mid_hop)

        self.assertTrue(node.state.game_over)
        self.assertEqual(node.state.turn, BLUE)
        self.assertEqual(node.state.whoWon(), RED)
        self.assertEqual(node.state.move_count, 1)

    def test_double_jump_plus_one(self):
        b = double_jump_board_plus_ones()
        state = GameState(board=b, turn=RED)
        node = Node(state)

        # self.assertTrue(Action(from_x=0, from_y=0, to_x=2, to_y=2) in node.next_actions())
        self.assertEqual(set(node.next_actions()), {Action(from_x=0, from_y=0, to_x=2, to_y=2),
                                                    Action(from_x=0, from_y=6, to_x=1, to_y=7)})
        node = node.next_node(Action(from_x=0, from_y=0, to_x=2, to_y=2))
        self.assertTrue(node.state.mid_hop)
        self.assertFalse(node.state.game_over)
        self.assertEqual(node.state.turn, RED)

        # self.assertTrue(Action(from_x=2, from_y=2, to_x=4, to_y=4) in node.next_actions())
        self.assertEqual(set(node.next_actions()), {Action(from_x=2, from_y=2, to_x=4, to_y=4)})
        node = node.next_node(Action(from_x=2, from_y=2, to_x=4, to_y=4))
        self.assertFalse(node.state.mid_hop)
        self.assertEqual(node.state.turn, BLUE)

        self.assertFalse(node.state.game_over)
        self.assertEqual(node.state.whoWon(), None)
        self.assertEqual(node.state.move_count, 1)

        self.assertEqual(set(node.next_actions()), {Action(from_x=5, from_y=3, to_x=4, to_y=2),
                                                    Action(from_x=5, from_y=3, to_x=6, to_y=2)})


def double_jump_board() -> Board:
    # RED can double jump from (0,0) => (2,2) => (4,4)

    b = Board()

    # empty the matrix
    for x in range(8):
        for y in range(8):
            b.matrix[y][x].occupant = None

    b.matrix[0][0].occupant = Piece(RED)
    b.matrix[1][1].occupant = Piece(BLUE)
    b.matrix[3][3].occupant = Piece(BLUE)

    return b


def double_jump_board_plus_ones() -> Board:
    b = double_jump_board()
    b.matrix[5][3].occupant = Piece(BLUE)
    b.matrix[0][6].occupant = Piece(RED)
    return b
