import unittest

import utils

import day07


class TestDay07(unittest.TestCase):
    """Day 07 test cases"""

    def test_first(self):
        start_positions = utils.parse_line("test_input.txt", ",", int)
        self.assertEqual(day07.find_min_fuel(start_positions), 37)

    def test_second(self):
        start_positions = utils.parse_line("test_input.txt", ",", int)
        self.assertEqual(day07.find_min_fuel(start_positions, True), 168)
