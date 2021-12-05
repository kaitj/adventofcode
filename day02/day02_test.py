import unittest

import utils

import day02


class TestDay02(unittest.TestCase):
    """Day 02 test cases"""

    def test_first(self):
        data = utils.parse_group("test_input.txt")
        self.assertEqual(day02.travel(data), 150)

    def test_second(self):
        data = utils.parse_group("test_input.txt")
        self.assertEqual(day02.travel(data, True), 900)


if __name__ == "__main__":
    unittest.main()
