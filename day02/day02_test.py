import unittest

import utils

import day02


class TestDay02(unittest.TestCase):
    """Day 02 test cases"""

    def test_first(self):
        data = utils.parse_group("test_input.txt")

        x_pos, y_pos = day02.planned_course(data)
        self.assertEqual(x_pos * y_pos, 150)

    def test_second(self):
        data = utils.parse_group("test_input.txt")

        x_pos, y_pos = day02.planned_course(data, aim=0)
        self.assertEqual(x_pos * y_pos, 900)


if __name__ == "__main__":
    unittest.main()
