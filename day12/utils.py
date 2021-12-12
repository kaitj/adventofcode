def parse_lines(filepath: str) -> list[type]:
    with open(filepath, "r", encoding="utf-8") as fpath:
        data = [line.strip("\n") for line in fpath]

    return data
