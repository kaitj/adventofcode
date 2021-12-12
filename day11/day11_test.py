import unittest

import utils

import day11


class TestDay11(unittest.TestCase):
    """Day 11 test cases"""

    def test_first(self):
        in_data = utils.parse_lines("test_input.txt", int)
        self.assertEqual(day11.puzzle1(in_data), 204)
        self.assertEqual(day11.puzzle1(in_data, 100), 1656)

    def test_second(self):
        in_data = utils.parse_lines("test_input.txt", int)
        self.assertEqual(day11.puzzle2(in_data), 195)
