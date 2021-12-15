from collections import Counter

import utils


class Polymer:
    """Class to build and counter polymer chain"""

    def __init__(self, in_template: str, in_pairs: list[str]):
        self.template = in_template
        self.rules = {pair.split(" -> ")[0]: pair.split(" -> ")[1] for pair in in_pairs}

        # Use a counter to keep track of pair frequency
        self.frequency = Counter()
        for idx in range(len(in_template) - 1):
            self.frequency[in_template[idx] + in_template[idx + 1]] += 1

    def build(self, steps: int = 0):
        for step in range(steps + 1):
            # If final step, count last character
            if step == steps:
                final_frequency = Counter()
                for char in self.frequency:
                    final_frequency[char[0]] += self.frequency[char]
                final_frequency[self.template[-1]] += 1
                self.frequency = final_frequency
                break

            # Count new pairs
            new_freq = Counter()
            for char in self.frequency:
                new_freq[char[0] + self.rules[char]] += self.frequency[char]
                new_freq[self.rules[char] + char[1]] += self.frequency[char]
            self.frequency = new_freq

    def get_common(self):
        return max(self.frequency.values()), min(self.frequency.values())


def puzzle(in_template: str, in_pairs: list[str], steps: int) -> int:
    polymer = Polymer(in_template, in_pairs)
    polymer.build(steps)
    mc, lc = polymer.get_common()

    return mc - lc


if __name__ == "__main__":
    in_fpath = input("Enter file containing manual: ")
    template, pairs = utils.parse_lines(in_fpath)

    # Puzzle 1
    print(
        f"The difference between most and least common element is: {puzzle(template, pairs, 10)}"
    )

    # Puzzle 2
    print(
        f"The difference between most and least common element is: {puzzle(template, pairs, 40)}"
    )
