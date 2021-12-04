import unittest

import utils

import day04


class TestDay04(unittest.TestCase):
    """Day 04 test cases"""

    def test_first(self):
        data = utils.parse_group("test_input.txt")
        draw_nums = day04.get_draw(data[0])
        boards = day04.gen_boards(data[1:])
        winning_board, draw = day04.play_bingo(draw_nums, boards)
        self.assertEqual(
            draw * sum(ele.num for ele in winning_board.values() if not ele.drawn), 4512
        )

    def test_second(self):
        data = utils.parse_group("test_input.txt")
        draw_nums = day04.get_draw(data[0])
        boards = day04.gen_boards(data[1:])
        winning_board, draw = day04.play_bingo(draw_nums, boards, True)
        self.assertEqual(
            draw * sum(ele.num for ele in winning_board.values() if not ele.drawn), 1924
        )
