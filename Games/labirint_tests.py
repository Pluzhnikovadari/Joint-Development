"""Test for labirinth."""
import unittest
from labirint import intersect_line_circle, point_in_rect, point_in_circle


class TestGame(unittest.TestCase):
    """Class test."""

    def test_intersect_line_circle(self):
        """Line intersects circle."""
        self.assertTrue(intersect_line_circle(0, 0, 10, -10, 10, 10, 10))

    def test_intersect_line_circle2(self):
        """Line doesn't intersect circle."""
        self.assertFalse(intersect_line_circle(0, 0, 10, -10, 10, 10, 11))

    def test_point_in_rect(self):
        """Point is inside rectangle."""
        pos = (5, 5)
        start = (0, 0)
        params = (10, 10)
        self.assertTrue(point_in_rect(pos, start, params))

    def test_point_in_rect2(self):
        """Point isn't inside rectangle."""
        pos = (5, 5)
        start = (0, 10)
        params = (10, 10)
        self.assertFalse(point_in_rect(pos, start, params))

    def test_point_in_circle(self):
        """Point is inside rectangle."""
        pos = (6, 8)
        start = (0, 0)
        radius = 10
        self.assertTrue(point_in_circle(pos, start, radius))

    def test_point_in_circle2(self):
        """Point isn't inside rectangle."""
        pos = (5, -9)
        start = (0, 0)
        radius = 10
        self.assertFalse(point_in_circle(pos, start, radius))


if __name__ == "__main__":
    unittest.main()
