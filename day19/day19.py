#!/usr/bin/env python
import re
from pathlib import Path
from typing import Self


class Blueprint:
    __slots__ = ("id", "cost", "useful")

    def __init__(self: Self, input_string: str) -> None:
        vals = [int(i) for i in re.findall(r"\d+", input_string)]
        self.id = vals[0]
        self.cost = {
            "ore": {"ore": vals[1]},
            "clay": {"ore": vals[2]},
            "obsidian": {"ore": vals[3], "clay": vals[4]},
            "geode": {"ore": vals[5], "obsidian": vals[6]},
        }
        self.useful = {
            "ore": max(
                self.cost["clay"]["ore"],
                self.cost["obsidian"]["ore"],
                self.cost["geode"]["ore"],
            ),
            "clay": self.cost["obsidian"]["clay"],
            "obsidian": self.cost["geode"]["obsidian"],
            "geode": float("inf"),
        }


class State:
    __slots__ = ("robots", "resources", "ignored")

    def __init__(
        self: Self,
        robots: dict[str, int] | None = None,
        resources: dict[str, int] | None = None,
        ignored: list[str] | None = None,
    ):
        self.robots = (
            robots.copy()
            if robots
            else {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        )
        self.resources = (
            resources.copy()
            if resources
            else {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        )
        self.ignored = ignored.copy() if ignored else []

    def copy(self: Self) -> "State":
        return State(self.robots, self.resources, self.ignored)

    def __gt__(self: Self, other: Self) -> bool:
        return self.resources["geode"] > other.resources["geode"]

    def __repr__(self: Self) -> str:
        return f"{{robots: {self.robots}, resources: {self.resources}}}"


def evaluate_options(
    blueprint: Blueprint, prior_states: list[State], timelimit: int = 26
) -> list[tuple[int, list[State]]]:
    time_remaining: int = timelimit - len(prior_states)
    curr_state = prior_states[-1]

    # determine options for what to build in the next state
    options: list[str] = []
    if time_remaining >= 0:
        # look for something affordable and useful and not ignored last time
        for robot, cost in blueprint.cost.items():
            if (
                curr_state.robots[robot] < blueprint.useful[robot]
                and all(curr_state.resources[k] >= v for k, v in cost.items())
                and robot not in curr_state.ignored
            ):
                options.append(robot)

        # geodes before anything else, don't bother with other types at the end
        if "geode" in options:
            options = ["geode"]
        elif time_remaining < 1:
            options = []
        else:
            # cutting off plans that build resources more than 2 phases back
            if (
                curr_state.robots["clay"] > 3
                or curr_state.robots["obsidian"]
                or "obsidian" in options
            ) and "ore" in options:
                options.remove("ore")
            if (
                curr_state.robots["obsidian"] > 3
                or curr_state.robots["geode"]
                or "geode" in options
            ) and "clay" in options:
                options.remove("clay")

        # add new resources
        next_state = curr_state.copy()
        for r, n in next_state.robots.items():
            next_state.resources[r] += n

        # the 'do nothing' option
        next_state.ignored += options
        results = [  # type: ignore
            evaluate_options(blueprint, prior_states + [next_state], timelimit)
        ]

        # the rest of the options
        for opt in options:
            next_state_opt = next_state.copy()
            next_state_opt.ignored = []
            next_state_opt.robots[opt] += 1
            for r, n in blueprint.cost[opt].items():
                next_state_opt.resources[r] -= n
            results.append(  # type: ignore
                evaluate_options(blueprint, prior_states + [next_state_opt], timelimit)
            )

        return max(results)  # type: ignore

    return prior_states[-1].resources["geode"], prior_states  # type: ignore


def parse_input(input_path: Path) -> list[Blueprint]:
    with input_path.open(encoding="utf-8") as in_file:
        blueprints = [Blueprint(bp.strip()) for bp in in_file]
    return blueprints


def solve_p1(blueprints: list[Blueprint]) -> int:
    res = 0
    for bp in blueprints:
        r = evaluate_options(bp, [State()], 24)
        res += r[0] * bp.id  # type: ignore
    return res  # type: ignore


def solve_p2(blueprints: list[Blueprint]) -> int:
    if len(blueprints) > 3:
        blueprints = blueprints[:3]
    res = 1
    for bp in blueprints:
        r = evaluate_options(bp, [State()], 32)
        res *= r[0]  # type: ignore
    return res  # type: ignore


if __name__ == "__main__":
    in_file = Path(__file__).parent.joinpath("input.txt")
    blueprints = parse_input(in_file)

    # Part 1
    print(f"Quality level of all blueprints in list: {solve_p1(blueprints)}")

    # Part 2
    print(f"Largest number of geodes with first 3 blueprints: {solve_p2(blueprints)}")
