import unittest

import utils

import day06


class TestDay06(unittest.TestCase):
    """Day 06 test cases"""

    def test_first(self):
        fish_dates = utils.parse_line("test_input.txt", ",", int)
        self.assertEqual(day06.count_fish(fish_dates, 18), 26)
        self.assertEqual(day06.count_fish(fish_dates, 80), 5934)

    def test_second(self):
        fish_dates = utils.parse_line("test_input.txt", ",", int)
        self.assertEqual(day06.count_fish(fish_dates, 256), 26984457539)
