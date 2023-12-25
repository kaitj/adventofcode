#!/usr/bin/env python
import itertools as it
import re
from pathlib import Path
from typing import Any


def read_input(in_file: str) -> list[list[str]]:
    """Read input file"""

    with Path(in_file).open(encoding="utf-8") as in_path:
        return [re.findall(r"[A-Z]+|\d+", line[1:]) for line in in_path]


def solve(puzzle: list[list[str]], part2: bool = False) -> int:
    graph = {valve: leads for valve, _, *leads, in puzzle}
    flows = {valve: int(flow) for valve, flow, *_ in puzzle if int(flow) > 0}
    indices = {valve: 1 << idx for idx, valve in enumerate(flows)}
    distances = {
        (node1, node2): 1 if node2 in graph[node1] else 1000
        for node2 in graph
        for node1 in graph
    }

    # Floyd-warshall - distance for any possible pair of valves
    for node1, node2, node3 in it.permutations(graph, 3):
        distances[node2, node3] = min(
            distances[node2, node3], distances[node1, node2] + distances[node1, node3]
        )

    def visit(
        valve: str, minutes: int, bitmask: int, pressure: int, ans: dict[Any, int]
    ):
        ans[bitmask] = max(ans.get(bitmask, 0), pressure)

        for valve2, flow in flows.items():
            rem_time = minutes - distances[valve, valve2] - 1

            if indices[valve2] & bitmask or rem_time <= 0:
                continue

            visit(
                valve=valve2,
                minutes=rem_time,
                bitmask=bitmask | indices[valve2],
                pressure=pressure + flow * rem_time,
                ans=ans,
            )

        return ans

    if not part2:
        return max(visit("AA", 30, 0, 0, {}).values())
    else:
        visited2 = visit("AA", 26, 0, 0, {})
        return max(
            v1 + v2
            for idx1, v1 in visited2.items()
            for idx2, v2 in visited2.items()
            if not idx1 & idx2
        )


if __name__ == "__main__":
    in_file = str(Path(__file__).parent.joinpath("input.txt"))
    valve_info = read_input(in_file)

    # Part 1
    print(f"Most pressure that can be released: {solve(valve_info)}")

    # Part 2
    print(f"Most pressure that can be released: {solve(valve_info, True)}")
