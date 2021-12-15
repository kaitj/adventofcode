import unittest

import utils

import day14


class Day14Test(unittest.TestCase):
    """Day 14 unit tests"""

    def test_first(self):
        template, pairs = utils.parse_lines("test_input.txt")
        self.assertEqual(day14.puzzle(template, pairs, 10), 1588)

    def test_second(self):
        template, pairs = utils.parse_lines("test_input.txt")
        self.assertEqual(day14.puzzle(template, pairs, 40), 2188189693529)
