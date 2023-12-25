#!/usr/bin/env python
from copy import copy, deepcopy
from pathlib import Path
from random import shuffle
from typing import Self

from aoc.utils import day_parser


class Day25:
    def __init__(self: Self, input_path: str):
        self.graph = self.load_graph(input_path)

    def load_graph(self: Self, input_path: str):
        graph: dict[str, set[str]] = {}
        with Path(input_path).open(encoding="utf-8") as in_file:
            for line in in_file:
                node, neighbours = line.split(": ")
                neighbours = set(neighbours.split())

                graph.setdefault(node, set()).update(neighbours)

                for n_node in neighbours:
                    graph.setdefault(n_node, set()).add(node)
        return graph

    # Return product of cardinality of two remaining nodes after
    # contracting to "target" edges or fewer
    def min_cut(self: Self, *, target: int):
        edges: list[list[str]] = []
        graph = deepcopy(self.graph)

        # Create new representation of edges
        for node, neighbours in graph.items():
            for neighbour in copy(neighbours):
                edge = [node, neighbour]
                edges.append(edge)
                neighbours.discard(neighbour)
                graph[neighbour].discard(node)
        saved = edges

        # Run Karger until solution found
        while True:
            edges = deepcopy(saved)
            nodes: dict[str, list[list[str]]] = {}

            for edge in edges:
                a, b = edge
                nodes.setdefault(a, []).append(edge)
                nodes.setdefault(b, []).append(edge)
            node_sz = {node: 1 for node in nodes}

            # Shuffle and pop off the end
            shuffle(edges)
            while len(nodes) > 2:
                edge = edges.pop()
                a, b = edge
                # Skip self edges
                if a == b:
                    continue

                # Move edges from b to a and rename
                for edge in nodes[b]:
                    for i in range(2):
                        if edge[i] == b:
                            edge[i] = a
                    nodes[a].append(edge)
                del nodes[b]

                # Update node_sz
                node_sz[a] += node_sz[b]
                del node_sz[b]

                # Remove self edges in a
                new_edges = [edge for edge in nodes[a] if edge[0] != edge[1]]
                nodes[a] = new_edges

            keys = list(nodes)
            if len(nodes[keys[0]]) <= target:
                break

        return node_sz[keys[0]] * node_sz[keys[1]]


class TestMain:
    def test_part1(self) -> None:
        test = Day25(f"{Path(__file__).parent}/test_input_part1.txt")
        assert test.min_cut(target=3) == 54

    def test_part2(self) -> None:
        raise NotImplementedError()
        # test = Day25(f"{Path(__file__).parent}/test_input_part2.txt")


def main():
    args = day_parser().parse_args()

    solution = Day25(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        print(solution.min_cut(target=3))
    elif args.part == 2:
        raise NotImplementedError()
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
