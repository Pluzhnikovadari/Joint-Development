"""Tests for tictactoe."""
import unittest
from tic import Game


class TestGame(unittest.TestCase):
    """Test class."""

    def setUp(self):
        """Create game object."""
        self.tictac = Game()

    def test_check1(self):
        """Check for player2 is winner."""
        self.tictac.mas = [['o', 'x', 0], ['o', 'x', 0], ['o', 0, 0]]
        self.assertEqual(self.tictac.check_winner(), 'Second player wins')

    def test_check2(self):
        """Check for player1 is winner."""
        self.tictac.mas = [[0, 'x', 'o'], [0, 'x', 'o'], [0, 'x', 0]]
        self.assertEqual(self.tictac.check_winner(), 'First player wins')

    def test_check3(self):
        """Check for draw."""
        self.tictac.mas = [['x', 'o', 'x'], ['o', 'x', 'x'], ['o', 'x', 'o']]
        self.tictac.query = 9
        self.assertEqual(self.tictac.check_winner(), 'Draw')


if __name__ == "__main__":
    unittest.main()
