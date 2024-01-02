from pathlib import Path


def parse_input(in_fpath: Path) -> list[str]:
    with in_fpath.open() as in_file:
        return in_file.read().split()


def solve(puzzle: list[str]) -> int:
    width = len(puzzle[0])
    height = len(puzzle)

    m = 0
    finished = False
    while not finished:
        finished = True

        puzzle_new: list[str] = []
        for s in puzzle:
            if s[width - 1] + s[0] == ">.":
                s = "p" + s[1 : width - 1] + ":"
            puzzle_new += [s.replace(">.", ".>").replace(":", ".").replace("p", ">")]

            if puzzle_new[-1] != s:
                finished = False

        puzzle = ["".join(ch) for ch in zip(*puzzle_new)]
        puzzle_new: list[str] = []
        for s in puzzle:
            if s[height - 1] + s[0] == "v.":
                s = "p" + s[1 : height - 1] + ":"
            puzzle_new += [s.replace("v.", ".v").replace(":", ".").replace("p", "v")]

            if puzzle_new[-1] != s:
                finished = False

        puzzle = ["".join(ch) for ch in zip(*puzzle_new)]

        m += 1
    return m


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    puzzle = parse_input(in_fpath)

    print(f"Answer: {solve(puzzle)}")
