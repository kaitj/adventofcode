#!/usr/bin/env python
from pathlib import Path


class Node(object):
    def __init__(self, num: str):
        self.num = int(num)


def parse_input(input_path: Path) -> list[Node]:
    with input_path.open(encoding="utf-8") as in_file:
        nodes = list(map(Node, (line.strip() for line in in_file)))

    return nodes


def solve(nodes: list[Node], *, iterations: int = 1) -> int:
    length = len(nodes)
    seq = nodes.copy()

    for _ in range(iterations):
        for node in nodes:
            idx = seq.index(node)
            new_idx = (idx + node.num) % (length - 1)
            seq.insert(new_idx, seq.pop(idx))

    zero = next(idx for idx, node in enumerate(seq) if node.num == 0)
    answer = 0
    for offset in 1000, 2000, 3000:
        idx = (zero + offset) % length
        answer += seq[idx].num
    return answer


if __name__ == "__main__":
    in_file = Path(__file__).parent.joinpath("input.txt")
    nodes = parse_input(in_file)

    # Part 1
    print(f"Sum of three numbers: {solve(nodes)}")

    # Part 2
    for node in nodes:
        node.num *= 811589153
    print(f"Sum of three numbers: {solve(nodes, iterations=10)}")
