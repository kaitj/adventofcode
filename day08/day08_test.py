import unittest

import utils

import day08


class TestDay08(unittest.TestCase):
    """Day 08 test cases"""

    def test_first(self):
        in_data = utils.parse_lines("test_input.txt", str)
        self.assertEqual(day08.puzzle1(in_data), 26)

    def test_second(self):
        in_data = utils.parse_lines("test_input.txt", str)
        self.assertEqual(day08.puzzle2(in_data), 61229)
