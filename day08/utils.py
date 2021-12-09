def parse_lines(filepath: str, parse_type: type) -> list[type]:
    with open(filepath, "r", encoding="utf-8") as fpath:
        data = [parse_type(line) for line in fpath]

    return data
