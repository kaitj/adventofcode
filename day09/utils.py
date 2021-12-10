def parse_lines(filepath: str, parse_type: type) -> list[type]:
    with open(filepath, "r", encoding="utf-8") as fpath:
        data = [list(map(parse_type, line.strip("\n"))) for line in fpath]

    return data
