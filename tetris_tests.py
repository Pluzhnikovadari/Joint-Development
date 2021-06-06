"""Tetris tests."""
import unittest
from tetris import check_lost, create_grid, convert_shape_format, Piece
from forms import T


class TestGame(unittest.TestCase):
    """Test class."""

    def test_check1(self):
        """Losing check."""
        pos = [(i, i + 1) for i in range(10)]
        self.assertFalse(check_lost(pos))

    def test_check2(self):
        """Losing check."""
        pos = [(i, i - 18) for i in range(10)]
        self.assertTrue(check_lost(pos))

    def test_create_grid(self):
        """Creating check."""
        loc = {}
        grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in loc:
                    grid[i][j] = 0
        self.assertEqual(create_grid(loc), grid)

    def test_convert_shape_format(self):
        """Converting check."""
        d = Piece(5, 0, T)
        self.assertEqual(convert_shape_format(d), [(5, -3), (4, -2),
                                                   (5, -2), (6, -2)])


if __name__ == "__main__":
    unittest.main()
