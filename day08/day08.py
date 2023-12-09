#!/usr/bin/env python
import math
import re
from dataclasses import dataclass
from pathlib import Path
from unittest import TestCase


@dataclass
class Node:
    node: str
    left: str
    right: str


class Day08:
    def __init__(self, input_path: str):
        self.network = self.load_network(input_path)

    def load_network(self, input_path: str) -> dict[str, str | dict[str, Node]]:
        network: dict[str, str | dict[str, Node]] = {}
        with Path(input_path).open(encoding="utf-8") as in_file:
            content = in_file.read().split("\n\n")

        network["instructions"] = content[0]

        nodes = (re.findall(r"(\w+)", node) for node in content[1].split("\n"))
        network["nodes"] = {
            line[0]: Node(node=line[0], left=line[1], right=line[2]) for line in nodes
        }

        return network

    def find_steps_to_finish(self, start_node: str) -> int:
        steps = 0
        cur_node = self.network["nodes"].get(start_node)  # pyright: ignore
        num_instructions = len(self.network["instructions"])

        while not cur_node.node.endswith("Z"):  # pyright: ignore
            cur_node = self.network["nodes"].get(  # pyright: ignore
                cur_node.right  # pyright: ignore
                if self.network["instructions"][
                    steps % num_instructions
                ]  # pyright: ignore
                == "R"
                else cur_node.left,  # pyright: ignore
                None,
            )
            steps += 1

        return steps


class TestMain(TestCase):
    def test_part1(self):
        test = Day08(f"{Path(__file__).parent}/test_input_part1.txt")
        self.assertEqual(test.find_steps_to_finish("AAA"), 2)

    def test_part2(self):
        test = Day08(f"{Path(__file__).parent}/test_input_part2.txt")
        start_nodes = ["11A", "22A"]
        self.assertEqual(
            math.lcm(*[test.find_steps_to_finish(node) for node in start_nodes]),
            6,
        )


if __name__ == "__main__":
    solution = Day08(f"{Path(__file__).parent}/input.txt")
    print(solution.find_steps_to_finish("AAA"))
    start_nodes = [  # pyright: ignore
        node
        for node in solution.network["nodes"].keys()  # pyright: ignore
        if node.endswith("A")  # pyright: ignore
    ]
    print(
        math.lcm(
            *[
                solution.find_steps_to_finish(node)  # pyright: ignore
                for node in start_nodes  # pyright: ignore
            ]
        )
    )
