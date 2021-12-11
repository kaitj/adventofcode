from typing import Generator

import utils


class Stack:
    """Class containing information about a line stack"""

    def __init__(self):
        self.__items = []

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        return self.__items.pop()

    def peek(self):
        return self.__items[-1]

    def is_empty(self):
        return len(self.__items) == 0


class SyntaxSearch:
    """Class for searching and scoring invalid lines"""

    def __init__(self):
        self.matching_pairs = {")": "(", "}": "{", "]": "[", ">": "<"}

        self.points = {")": 3, "]": 57, "}": 1197, ">": 25137}

    def score_missing(self, line: list[str]) -> int:
        syntax_stack = Stack()

        for char in line:
            if char in self.matching_pairs.values():
                syntax_stack.push(char)
            elif char in self.matching_pairs.keys():
                if syntax_stack.pop() != self.matching_pairs[char]:
                    return self.points[char]
            else:
                raise ValueError(f"Invalid character {char}")

        return 0


class SyntaxComplete:
    """Class for searching and scoring lines that need tto be auto completed"""

    def __init__(self):
        self.matching_pairs = {")": "(", "}": "{", "]": "[", ">": "<"}

        self.points = {"(": 1, "[": 2, "{": 3, "<": 4}

    def autocomplete(self, line: list[str]) -> int:
        syntax_stack = Stack()

        for char in line:
            if char in self.matching_pairs.values():
                syntax_stack.push(char)
            elif char in self.matching_pairs.keys():
                if syntax_stack.peek() != self.matching_pairs[char]:
                    raise ValueError(f"Invalid line: {line}")
                syntax_stack.pop()

        score = 0
        while not syntax_stack.is_empty():
            score *= 5
            score += self.points[syntax_stack.pop()]

        return score

    def score_lines(self, lines: list[str]) -> Generator[int, None, None]:
        for line in lines:
            try:
                yield self.autocomplete(line)
            except ValueError:
                continue

    def winning_line_score(self, lines: list) -> int:
        scores = sorted(self.score_lines(lines))
        return scores[len(scores) // 2]


def puzzle1(data):
    analyzer = SyntaxSearch()

    return sum(analyzer.score_missing(line) for line in data)


def puzzle2(data):
    autocomplete = SyntaxComplete()

    return autocomplete.winning_line_score(data)


if __name__ == "__main__":
    in_fpath = input("Enter path containing syntax stack: ")
    in_data = utils.parse_lines(in_fpath, str)

    # Puzzle 1
    print(f"The total syntax error score is {puzzle1(in_data)}")

    # Puzzle 1
    print(f"The syntax autocomplete middle score is {puzzle2(in_data)}")
