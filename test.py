import unittest
from main import change_size


class TestChangeSize(unittest.TestCase):
    """
    Тестирование функции change_size
    """

    def test_change_size(self):
        # Проверка увеличения размера
        self.assertEqual(change_size(12, 9, 18, 0, 24, 232, 1), 13)
        self.assertEqual(change_size(12, 9, 18, 0, 24, 256, 4), 13)

        # Проверка уменьшения размера
        self.assertEqual(change_size(12, 9, 18, 0, 24, 280, 1), 11)
        self.assertEqual(change_size(12, 9, 18, 0, 24, 256, 5), 11)

        # Проверка верхнего предела
        self.assertEqual(change_size(18, 9, 18, 0, 24, 232, 1), 18)
        self.assertEqual(change_size(18, 9, 18, 0, 24, 256, 4), 18)

        # Проверка нижнего предела
        self.assertEqual(change_size(9, 9, 18, 0, 24, 280, 1), 9)
        self.assertEqual(change_size(9, 9, 18, 0, 24, 256, 5), 9)

        # Проверка нахождения курсора вне кнопки по оси X
        self.assertEqual(change_size(12, 9, 18, 0, 64, 232, 1), 12)
        self.assertEqual(change_size(12, 9, 18, 0, 64, 256, 4), 12)

        # Проверка нахождения курсора вне кнопки по оси Y
        self.assertEqual(change_size(12, 9, 18, 0, 24, 256, 1), 12)


if __name__ == '__main__':
    unittest.main()
