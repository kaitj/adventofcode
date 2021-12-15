def parse_lines(filepath: str):
    with open(filepath, "r", encoding="utf-8") as fpath:
        template, pairs = fpath.read().split("\n\n")
        pairs = pairs.split("\n")

        return template, pairs
