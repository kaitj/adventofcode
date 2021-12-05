from typing import Optional

import utils


class Position:
    """Position of submarine"""

    def __init__(self, horizontal: int, depth: int, aim: Optional[(int)] = None):
        self.horizontal = horizontal
        self.depth = depth
        self.aim = aim

    def execute(self, instruc: str):
        """Execute instruction on position"""
        direction, distance = instruc.split(" ")
        distance = int(distance)

        if self.aim is not None:
            match direction:
                case "forward":
                    self.horizontal += distance
                    self.depth += self.aim * distance
                case "up":
                    self.aim -= distance
                case "down":
                    self.aim += distance
        else:
            match direction:
                case "forward":
                    self.horizontal += distance
                case "up":
                    self.depth -= distance
                case "down":
                    self.depth += distance


def travel(instrucs: list[str], aim: bool = False) -> int:
    position = Position(0, 0, 0) if aim else Position(0, 0)

    for instruc in instrucs:
        position.execute(instruc)

    return position.horizontal * position.depth


if __name__ == "__main__":
    input_fpath = input("Enter path containing input commands: ")
    in_cmds = utils.parse_group(input_fpath)

    # Puzzle 1
    print(f"Depth x position = {travel(in_cmds)}")

    # Puzzle 2
    print(f"Depth * position (with aim) = {travel(in_cmds, True)}")
