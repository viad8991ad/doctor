import unittest
from app import random_result_analyzes, random_name_analyzes


class AnalyzesTest(unittest.TestCase):

    def test_analyzes_res(self):
        analyzes_list = ["POS", "NEG"]
        self.assertTrue(random_result_analyzes() in analyzes_list)

    def test_analyzes_name(self):
        analyzes_list = ["анализ 0", "анализ 1", "анализ 2", "анализ 3", "анализ 4", "анализ 5", ]
        self.assertTrue(random_name_analyzes() in analyzes_list)


if __name__ == '__main__':
    unittest.main()
