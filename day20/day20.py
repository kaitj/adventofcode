#!/usr/bin/env python
from dataclasses import dataclass, field
from math import prod
from pathlib import Path

from aoc.utils import day_parser


@dataclass
class Node:
    name: str
    type_: str
    dests: list[str]
    state: bool = False  # True (On) / False (Off)
    inputs: dict[str, bool] = field(default_factory=dict)


class Day20:
    def __init__(self, input_path: str) -> None:
        self.nodes = self.load_nodes(input_path)
        self.button_count = 0
        self.state_count = [0, 0]
        self.queue = []

    def load_nodes(self, input_path: str) -> dict[str, Node]:
        nodes: dict[str, Node] = {}

        with Path(input_path).open(encoding="utf-8") as in_file:
            for line in in_file:
                src, dests = line.strip().split(" -> ")
                dests = dests.split(", ")

                if src.startswith("b"):
                    node = Node(name=src, type_="b", dests=dests)
                else:
                    node = Node(name=src[1:], type_=src[0], dests=dests)
                nodes[node.name] = node

        nodes["rx"] = Node(name="rx", type_="r", dests=[])

        # Set all downstream nodes' state to false
        for vals in nodes.values():
            for node_dest in vals.dests:
                nodes[node_dest].inputs[vals.name] = False

        try:
            (self.parent,) = nodes["rx"].inputs.keys()
            self.listen = {node: None for node in nodes[self.parent].inputs.keys()}
        except ValueError:
            self.parent = None
            self.listen = {}

        return nodes

    def press_button(self) -> None:
        self.queue = [("button", "broadcaster", False)]  # src, dest, state
        self.button_count += 1
        while self.queue:
            self.process(*self.queue.pop(0))

    def process(self, src: str, dest: str, state: bool):
        self.state_count[state] += 1
        node = self.nodes[dest]

        if node.type_ == "%":
            if state:
                return
            node.state = not node.state
        elif node.type_ == "&":
            node.inputs[src] = state
            node.state = not all(node.inputs.values())

            if dest == self.parent:
                for key, val in self.listen.items():
                    if val is None and key == src and state:
                        self.listen[key] = self.button_count  # pyright: ignore

        for node_dest in node.dests:
            self.queue.append((dest, node_dest, node.state))  # pyright: ignore

    def press(self, presses: int) -> None:
        for _ in range(presses):
            self.press_button()


class TestMain:
    def test_part1(self) -> None:
        test = Day20(f"{Path(__file__).parent}/test_input_part1.txt")
        test.press(presses=1000)
        assert test.state_count == [8000, 4000]
        assert prod(test.state_count) == 32000000

    def test_part2(self) -> None:
        raise NotImplementedError()
        # test = Day20(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day20(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        solution.press(presses=1000)
        print(prod(solution.state_count))
    elif args.part == 2:
        raise NotImplementedError()
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
