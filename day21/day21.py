#!/usr/bin/env python
import re
from pathlib import Path

MONKEY_REGEX = re.compile(r"[a-z]{4}: (\d+|[a-z]{4} [-+*/] [a-z]{4})")


def parse_input(input_path: Path) -> dict[str, list[str]]:
    monkeys: dict[str, list[str]] = {}
    with input_path.open(encoding="utf-8") as in_file:
        for line in in_file:
            line = line.strip()
            if not MONKEY_REGEX.match(line):
                raise Exception("Can't eval")
            name, other = line.split(": ")
            monkeys[name] = other.split()

    return monkeys


def expand(monkeys: dict[str, list[str]], key: str) -> str:
    if len(monkeys[key]) == 3:
        one, op, other = monkeys[key]
        one = expand(monkeys, one)
        other = expand(monkeys, other)
        return "(%s %s %s)" % (one, op, other)
    elif len(monkeys[key]) == 1:
        return monkeys[key][0]
    else:
        # Handle other cases as needed
        raise ValueError("Invalid input format for key '%s'" % key)


def solve(monkeys: dict[str, list[str]]) -> int:
    return eval(expand(monkeys, "root"))  # type: ignore


if __name__ == "__main__":
    in_file = Path(__file__).parent.joinpath("input.txt")
    monkeys = parse_input(in_file)

    # Part 1
    print(f"Number yelled: {int(solve(monkeys))}")

    # Part 2
    monkeys["root"][1] = "-("
    monkeys["humn"] = ["-1j"]
    complex = eval(expand(monkeys, "root") + ")")
    print(f"Number yelled: {round(complex.real / complex.imag)}")
