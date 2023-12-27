import copy
import math
from pathlib import Path
from typing import Self


def add_to_rightmost_int(stack: list, x: int) -> list:
    """
    Add x to rightmost int in l
    if no int in l, do nothing
    return modified l
    """
    int_locations = [isinstance(i, int) for i in stack]
    if not any(int_locations):
        return stack
    int_locations.reverse()
    last_index = len(int_locations) - 1 - int_locations.index(True)
    stack[last_index] += x
    return stack


def add_to_leftmost_int(stack: list, x: int) -> list:
    """
    Add x to leftmost int in l
    if no int in l, do nothing
    return modified l
    """
    int_locations = [isinstance(i, int) for i in stack]
    if not any(int_locations):
        return stack
    index = int_locations.index(True)
    stack[index] += x
    return stack


class SFNumber:
    def __init__(self, snailfish_str: str) -> None:
        self.raw_number = copy.copy(snailfish_str)
        self._parse()

    def _parse(self):
        """Convert string to internal format"""
        self.number = []
        current_digit = ""
        for char in self.raw_number:
            if char.isdigit():
                current_digit += char
            else:
                if current_digit != "":
                    self.number.append(int(current_digit))
                    current_digit = ""
                if char != ",":
                    self.number.append(char)

    def __repr__(self) -> str:
        return f"SFNumber({self.__str__()})"

    def __str__(self) -> str:
        output = ""
        for char in self.number:
            if output:
                if output[-1] == "]" and char != "]":
                    output += ","
                elif output[-1].isdigit() and char != "]":
                    output += ","
            output += str(char)
        return output

    def _explode_one(self) -> bool:
        stack = []
        index = 0
        depth = 0
        while index < len(self.number):
            x = self.number[index]
            if x == "[" and depth == 4:
                # EXPLOSTION DETECTED
                left_number = self.number[index + 1]
                right_number = self.number[index + 2]
                left_portion = add_to_rightmost_int(stack, left_number)
                right_portion = add_to_leftmost_int(
                    self.number[index + 4 :], right_number
                )
                self.number = left_portion + [0] + right_portion
                return True
            else:
                if x == "[":
                    depth += 1
                elif x == "]":
                    depth -= 1
                stack.append(x)
            index += 1
        return False

    def _split_one(self) -> bool:
        stack = []
        index = 0
        while index < len(self.number):
            x = self.number[index]
            if isinstance(x, int) and x > 9:
                # SPLIT!
                left_number = math.floor(x / 2)
                right_number = math.ceil(x / 2)
                insert = ["[", left_number, right_number, "]"]
                self.number = stack + insert + self.number[index + 1 :]
                return True
            else:
                stack.append(x)
                index += 1
        return False

    def reduce(self) -> None:
        reduced = False
        while not reduced:
            if self._explode_one():
                continue
            if self._split_one():
                continue
            reduced = True

    def add(self, sf_number: Self) -> None:
        new_number = ["["]
        new_number += self.number
        new_number += sf_number.number
        new_number += ["]"]
        self.number = new_number

    def _one_magnitude_layer(self, number):
        index = 0
        new_number = []
        while index < len(number):
            if number[index] == "[" and number[index + 3] == "]":
                left_number = number[index + 1] * 3
                right_number = number[index + 2] * 2
                new_number.append(left_number + right_number)
                index += 4
            else:
                new_number.append(number[index])
                index += 1
        return new_number

    @property
    def magnitude(self) -> int:
        magnitude = copy.copy(self.number)
        while len(magnitude) > 1:
            magnitude = self._one_magnitude_layer(magnitude)
        return magnitude.pop()


def process_snail_list(numbers: list[str]) -> SFNumber:
    result_number = None
    for number in numbers:
        new_number = SFNumber(number)
        if result_number is None:
            result_number = new_number
        else:
            result_number.add(new_number)
        result_number.reduce()
    return result_number


def find_largest_magnitude(number_list: list[str]):
    max_magnitude = 0
    for left_index in range(len(number_list)):
        for right_index in range(len(number_list)):
            if left_index != right_index:
                left_number = SFNumber(number_list[left_index])
                right_number = SFNumber(number_list[right_index])
                left_number.add(right_number)
                left_number.reduce()
                magnitude = left_number.magnitude
                if magnitude > max_magnitude:
                    max_magnitude = magnitude
    return max_magnitude


def parse_input(in_fpath: Path) -> list[str]:
    with in_fpath.open() as in_file:
        return [line.strip() for line in in_file]


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    in_lines = parse_input(in_fpath)

    print(f"Answer: {(process_snail_list(in_lines)).magnitude}")
    print(f"Answer: {find_largest_magnitude(in_lines)}")
