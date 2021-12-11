import unittest

import utils

import day10


class TestDay09(unittest.TestCase):
    """Day 10 test cases"""

    def test_first(self):
        in_data = utils.parse_lines("test_input.txt", str)
        self.assertEqual(day10.puzzle1(in_data), 26397)

    def test_second(self):
        in_data = utils.parse_lines("test_input.txt", str)
        self.assertEqual(day10.puzzle2(in_data), 288957)
