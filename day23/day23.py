#!/usr/bin/env python
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from aoc.utils import day_parser


@dataclass
class Position:
    y: int
    x: int

    def __hash__(self) -> int:
        return hash((self.y, self.x))

    def __add__(self, other: "Position") -> "Position":
        return Position(y=self.y + other.y, x=self.x + other.x)


@dataclass
class Node:
    pos: Position
    edges: dict["Node", int]
    direction: Position | None

    def __hash__(self) -> int:
        return hash((self.pos, self.direction))


class Direction(Enum):
    U = Position(y=-1, x=0)
    D = Position(y=1, x=0)
    R = Position(y=0, x=1)
    L = Position(y=0, x=-1)


SLOPES = dict(zip("^v><", Direction))


class Day23:
    def __init__(self, input_path: str):
        self.map, self.start_pos, self.end_pos = self.load_map(input_path)
        self.create_graph()

    def load_map(
        self, input_path: str
    ) -> tuple[dict[Position, str], Position, Position]:
        map: dict[Position, str] = {}
        with Path(input_path).open(encoding="utf-8") as in_file:
            for y, row in enumerate(in_file):
                if y == 0:
                    start_pos = Position(y=y, x=row.index("."))
                for x, ch in enumerate(row.strip()):
                    map[Position(y=y, x=x)] = ch
            end_pos = Position(y=y, x=row.index("."))  # type: ignore

        return map, start_pos, end_pos  # type: ignore

    def create_graph(self):
        self.nodes: dict[Position, Node] = {}
        for pos, ch in self.map.items():
            if ch == ".":
                self.nodes[pos] = Node(pos=pos, edges={}, direction=None)
            if ch in SLOPES:
                self.nodes[pos] = Node(pos=pos, edges={}, direction=SLOPES[ch].value)

        self.start = self.nodes[self.start_pos]
        self.end = self.nodes[self.end_pos]

        # Find edges for each node
        for pos, node in self.nodes.items():
            for dir in Direction:
                if (npos := pos + dir.value) in self.nodes:
                    if self.nodes[npos].direction in (None, dir.value):
                        node.edges[self.nodes[npos]] = 1

        self.compress()

    def traverse(self) -> int:
        steps = 0
        q: list[tuple[Node, int, list[Node]]] = [(self.start, 0, [])]
        while q:
            node, dist, seen = q.pop(-1)

            if node == self.end:
                steps = max(steps, dist)

            for edge in node.edges:
                if edge not in seen:
                    q.append((edge, dist + node.edges[edge], [*seen, edge]))

        return steps

    def compress(self):
        for node in self.nodes.values():
            if node.direction is None:
                if len(node.edges) == 2 and not any(
                    edge.direction for edge in node.edges
                ):
                    node1, node2 = node.edges.keys()
                    del node1.edges[node], node2.edges[node]
                    node1.edges[node2] = sum(node.edges.values())
                    node2.edges[node1] = sum(node.edges.values())


class TestMain:
    def test_part1(self) -> None:
        test = Day23(f"{Path(__file__).parent}/test_input_part1.txt")
        test_steps = test.traverse()
        assert test_steps == 94

    def test_part2(self) -> None:
        raise NotImplementedError()
        # test = Day23(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day23(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        steps = solution.traverse()
        print(steps)
    elif args.part == 2:
        raise NotImplementedError()
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
