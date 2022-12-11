#!/usr/bin/env python3
import math
import re


class Monkey:
    def __init__(self, items, op, test, t, f, inspections=0):
        """Init monkey with input and 0 inspections"""
        self.items = items
        self.op = op
        self.test = test
        self.t = t
        self.f = f
        self.inspections = inspections

    def turn(self, limit, part):
        global monkeys
        while self.items:
            self.inspections += 1
            # Inspect current item
            cur_item = self.items.pop(0)
            worry = self.op(cur_item) // (3 if part == 1 else 1) % limit
            # Pass item to monkey, conditional on test pass/fail
            if worry % self.test == 0:
                monkeys[self.t].items.append(worry)
            else:
                monkeys[self.f].items.append(worry)


def build_op(operation):
    """Helper to build operation function"""
    # Multiply by value
    op_search = re.search(r"\w+: +\w+ = old \* (\d+)", operation)
    if op_search:
        return lambda x: x * int(op_search.group(1))

    op_search = re.search(r"\w+: +\w+ = old \+ (\d+)", operation)
    if op_search:
        return lambda x: x + int(op_search.group(1))

    op_search = re.search(r"\w+: +\w+ = old \* old", operation)
    if op_search:
        return lambda x: x * x


def read_input(in_file):
    """Read and sort input"""
    with open(in_file, "r") as f:
        monkey_info = f.read().split("\n\n")

    nums = re.compile(r"(\d+)")
    monkeys = []
    for monkey in monkey_info:
        info = monkey.split("\n")
        monkeys.append(
            Monkey(
                items=list(map(int, nums.findall(info[1]))),
                op=build_op(info[2]),
                test=int(nums.findall(info[3])[0]),
                t=int(nums.findall(info[4])[0]),
                f=int(nums.findall(info[5])[0]),
            )
        )

    return monkeys


def inspect(monkeys, rounds, part):
    """Perform inpsection round number of times"""
    limit = math.lcm(*[monkey.test for monkey in monkeys])

    for _ in range(rounds):
        for monkey in monkeys:
            monkey.turn(limit, part)

    return math.prod(sorted([monkey.inspections for monkey in monkeys])[-2:])


if __name__ == "__main__":
    in_file = str(input("Enter file containing monkey items: "))

    # Part 1
    monkeys = read_input(in_file)
    print(
        f"Level of monkey business after 20 rounds: {inspect(monkeys, 20, 1)}"
    )

    # Part 2
    monkeys = read_input(in_file)
    print(
        f"Level of monkey business after 10000 rounds: {inspect(monkeys, 10000, 2)}"
    )
