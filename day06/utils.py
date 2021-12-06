def parse_line(filepath: str, splitby: str, mapto: type) -> list[int]:
    with open(filepath, "r", encoding="utf-8") as fpath:
        data = fpath.read()

    data = [mapto(date) for date in data.split(splitby)]

    return data
