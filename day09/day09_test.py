import unittest

import utils

import day09


class TestDay09(unittest.TestCase):
    """Day 9 test cases"""

    def test_first(self):
        in_data = utils.parse_lines("test_input.txt", int)
        self.assertEqual(day09.puzzle1(in_data), 15)

    def test_second(self):
        in_data = utils.parse_lines("test_input.txt", int)
        self.assertEqual(day09.puzzle2(in_data), 1134)
