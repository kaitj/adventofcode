#!/usr/bin/env python
from dataclasses import dataclass
from pathlib import Path

from aoc.utils import day_parser


@dataclass(frozen=True)
class Node:
    conditions: list[str]
    rules: list[tuple[str] | tuple[str, str, int, str]]


class Day19:
    def __init__(self, input_path: str):
        self.load_workflows(input_path)
        self.start_condition = {
            "x": (1, 4000),
            "m": (1, 4000),
            "a": (1, 4000),
            "s": (1, 4000),
        }

    def load_workflows(
        self,
        input_path: str,
    ) -> None:
        self.workflow_nodes = {"A": Node([], []), "R": Node([], [])}

        self.parts: list[dict[str, int]] = []
        with Path(input_path).open(encoding="utf-8") as in_file:
            mode = "workflows"

            for line in in_file:
                if not line.strip():
                    mode = "ratings"
                    continue

                if mode == "workflows":
                    workflow, right = line.strip().split("{")
                    node = Node(conditions=[], rules=[])
                    for rule in right[:-1].split(","):
                        if ":" not in rule:
                            node.rules.append((rule,))
                            break
                        condition, child = rule.split(":")
                        var = condition[0]
                        symbol = condition[1]
                        value = int(condition[2:])
                        node.rules.append((var, symbol, value, child))
                    self.workflow_nodes[workflow] = node
                elif mode == "ratings":
                    rating_table: dict[str, int] = {}
                    for kv in line.strip()[1:-1].split(","):
                        rating_table[kv[0]] = int(kv[2:])
                    self.parts.append(rating_table)
                else:
                    raise ValueError("Invalid mode")

    def range_intersection(
        self, r1: tuple[int, int], r2: tuple[int, int]
    ) -> tuple[int, int] | None:
        left = max(r1[0], r2[0])
        right = min(r1[1], r2[1])

        if right < left:
            return None

        return left, right

    def process_node(self, node: Node, condition: str):
        node.conditions.append(condition)
        temp_condition = condition.copy()  # pyright: ignore

        for rule in node.rules:
            if len(rule) == 1:
                child_node = self.workflow_nodes[rule[0]]
                self.process_node(child_node, temp_condition)  # pyright: ignore
                continue
            var, symbol, value, child = rule
            interval = (1, value - 1) if symbol == "<" else (value + 1, 4000)
            child_temp_condition = temp_condition.copy()  # pyright: ignore
            child_temp_condition[var] = self.range_intersection(
                child_temp_condition[var],  # pyright: ignore
                interval,  # pyright: ignore
            )
            if child_temp_condition[var] is not None:
                child_node = self.workflow_nodes[child]
                self.process_node(child_node, child_temp_condition)  # pyright: ignore
            inverted_interval = (value, 4000) if symbol == "<" else (1, value)
            temp_condition[var] = self.range_intersection(
                temp_condition[var],  # pyright: ignore
                inverted_interval,  # pyright: ignore
            )
            if temp_condition[var] is None:
                break


class TestMain:
    def test_part1(self) -> None:
        test = Day19(f"{Path(__file__).parent}/test_input_part1.txt")
        test.process_node(
            test.workflow_nodes["in"],
            test.start_condition,  # pyright: ignore
        )
        test_ratings = [
            sum(part.values())
            for part in test.parts
            for condition in test.workflow_nodes["A"].conditions
            if all(
                condition[ch][0]  # pyright: ignore
                <= part[ch]
                <= condition[ch][1]  # pyright: ignore
                for ch in "xmas"
            )
        ]
        assert test_ratings == [7540, 4623, 6951]
        assert sum(test_ratings) == 19114

    def test_part2(self) -> None:
        test = Day19(f"{Path(__file__).parent}/test_input_part1.txt")
        test.process_node(
            test.workflow_nodes["in"],
            test.start_condition,  # pyright: ignore
        )
        total = 0
        for condition in test.workflow_nodes["A"].conditions:
            product = 1
            for p1, p2 in condition.values():  # pyright: ignore
                product *= p2 - p1 + 1  # pyright: ignore
            total += product  # pyright: ignore
        assert total == 167409079868000


def main():
    args = day_parser().parse_args()

    solution = Day19(f"{Path(__file__).parent}/input.txt")
    if args.part == 1:
        solution.process_node(
            solution.workflow_nodes["in"],
            solution.start_condition,  # pyright: ignore
        )
        print(
            sum(
                [
                    sum(part.values())
                    for part in solution.parts
                    for condition in solution.workflow_nodes["A"].conditions
                    if all(
                        condition[ch][0]  # pyright: ignore
                        <= part[ch]
                        <= condition[ch][1]  # pyright: ignore
                        for ch in "xmas"
                    )
                ]
            )
        )
    elif args.part == 2:
        solution.process_node(
            solution.workflow_nodes["in"],
            solution.start_condition,  # pyright: ignore
        )
        total = 0
        for condition in solution.workflow_nodes["A"].conditions:
            product = 1
            for p1, p2 in condition.values():  # pyright: ignore
                product *= p2 - p1 + 1  # pyright: ignore
            total += product  # pyright: ignore
        print(total)  # pyright: ignore
    else:
        raise ValueError("Not a valid part")


if __name__ == "__main__":
    main()
