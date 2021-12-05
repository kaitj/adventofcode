import unittest

import utils

import day05


class TestDay05(unittest.TestCase):
    """Day 05 test cases"""

    def test_first(self):
        data = utils.parse_lines("test_input.txt", str)
        self.assertEqual(day05.puzzle(data), 5)

    def test_second(self):
        data = utils.parse_lines("test_input.txt", str)
        self.assertEqual(day05.puzzle(data, True), 12)
