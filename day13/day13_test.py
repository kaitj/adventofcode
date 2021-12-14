import unittest

import utils

import day13


class Day13Test(unittest.TestCase):
    """Test cases for day 13"""

    def test_first(self):
        dots, instructions = utils.parse_lines("test_input.txt")
        self.assertEqual(day13.puzzle(dots, instructions, 1), 17)

    def test_second(self):
        dots, instructions = utils.parse_lines("test_input.txt")
        print(day13.puzzle(dots, instructions, None))
