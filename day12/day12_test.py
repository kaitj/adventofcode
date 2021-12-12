import unittest

import utils

import day12


class Day12Test(unittest.TestCase):
    """Day 12 test cases"""

    def test_first(self):
        test = [utils.parse_lines(f"test_input{i}.txt") for i in range(1, 4)]

        self.assertEqual(day12.puzzle(test[0]), 10)
        self.assertEqual(day12.puzzle(test[1]), 19)
        self.assertEqual(day12.puzzle(test[2]), 226)

    def test_second(self):
        test = [utils.parse_lines(f"test_input{i}.txt") for i in range(1, 4)]

        self.assertEqual(day12.puzzle(test[0], True), 36)
        self.assertEqual(day12.puzzle(test[1], True), 103)
        self.assertEqual(day12.puzzle(test[2], True), 3509)
