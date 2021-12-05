import unittest

import utils

import day01


class TestDay01(unittest.TestCase):
    """Day 01 test cases"""

    def test_first(self):
        data = utils.parse_lines("test_input.txt", int)
        self.assertEqual(day01.count_larger(data), 7)

    def test_second(self):
        data = utils.parse_lines("test_input.txt", int)
        windowed_data = day01.compute_window(data)
        self.assertEqual(day01.count_larger(windowed_data), 5)


if __name__ == "__main__":
    unittest.main()
