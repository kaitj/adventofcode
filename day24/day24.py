from pathlib import Path


def parse_input(in_fpath: Path) -> list[list[str]]:
    with in_fpath.open() as in_file:
        return [line.split() for line in in_file]


def get_relevant_adds(
    puzzle: list[list[str]],
) -> tuple[list[int | None], list[int | None]]:
    div1: list[None | int] = []
    div26: list[None | int] = []

    for idx in range(0, len(puzzle), 18):
        if puzzle[idx + 4][2] == "1":
            div1.append(int(puzzle[idx + 15][2]))
            div26.append(None)
        else:
            div1.append(None)
            div26.append(int(puzzle[idx + 5][2]))

    return div1, div26


def get_model_no(
    div1: list[int | None], div26: list[int | None], part_two: bool = False
):
    model_no = [0] * 14
    stack: list[tuple[int, int]] = []
    start_digit = 9 if not part_two else 1

    for idx, (a, b) in enumerate(zip(div1, div26)):
        if a:
            stack.append((idx, a))
        else:
            ia, a = stack.pop()
            diff: int = a + b  # type: ignore

            if not part_two:
                model_no[ia] = min(start_digit, start_digit - diff)  # type: ignore
                model_no[idx] = min(start_digit, start_digit + diff)  # type: ignore
            else:
                model_no[ia] = max(start_digit, start_digit - diff)  # type: ignore
                model_no[idx] = max(start_digit, start_digit + diff)  # type: ignore

    return model_no


def solve(puzzle: list[list[str]], part_two: bool = False):
    div1, div26 = get_relevant_adds(puzzle)
    return "".join(map(str, get_model_no(div1, div26, part_two)))


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    puzzle = parse_input(in_fpath)

    print(f"Answer: {solve(puzzle)}")
    print(f"Answer: {solve(puzzle, True)}")
