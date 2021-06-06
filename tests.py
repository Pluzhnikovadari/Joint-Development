"""Тесты крестики-нолики."""
import unittest
from tic import Game


class TestGame(unittest.TestCase):
    """Класс-тест."""

    def setUp(self):
        """Создание объекта-игры."""
        self.tictac = Game()

    def test_check1(self):
        """Проверка на победителя игрока2."""
        self.tictac.mas = [['o', 'x', 0], ['o', 'x', 0], ['o', 0, 0]]
        self.assertEqual(self.tictac.check_winner(), 'Second player wins')

    def test_check2(self):
        """Проверка на победителя игрока1."""
        self.tictac.mas = [[0, 'x', 'o'], [0, 'x', 'o'], [0, 'x', 0]]
        self.assertEqual(self.tictac.check_winner(), 'First player wins')

    def test_check3(self):
        """Проверка на ничью."""
        self.tictac.mas = [['x', 'o', 'x'], ['o', 'x', 'x'], ['o', 'x', 'o']]
        self.tictac.query = 9
        self.assertEqual(self.tictac.check_winner(), 'Draw')


if __name__ == "__main__":
    unittest.main()
