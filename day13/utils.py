def parse_lines(filepath: str) -> list:
    with open(filepath, "r", encoding="utf-8") as fpath:
        dots, instructions = fpath.read().split("\n\n")

    return dots, instructions
