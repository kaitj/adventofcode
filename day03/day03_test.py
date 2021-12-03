import unittest

import utils

import day03


class TestDay03(unittest.TestCase):
    """Day 03 test cases"""

    def test_first(self):
        data = utils.parse_group("test_input.txt")
        bit_counter = day03.count_bits(data)
        gamma = day03.compute_gamma(bit_counter)
        self.assertEqual(int(gamma, 2), 22)
        epsilon = day03.compute_epsilon(bit_counter)
        self.assertEqual(int(epsilon, 2), 9)

        self.assertEqual(int(gamma, 2) * int(epsilon, 2), 198)

    def test_second(self):
        data = utils.parse_group("test_input.txt")
        o2 = day03.compute_o2(data)
        self.assertEqual(int(o2, 2), 23)
        co2 = day03.compute_co2(data)
        self.assertEqual(int(co2, 2), 10)

        self.assertEqual(int(o2, 2) * int(co2, 2), 230)


if __name__ == "__main__":
    unittest.main()
