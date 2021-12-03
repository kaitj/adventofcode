def parse_group(filepath):
    with open(filepath, "r", encoding="utf-8") as fpath:
        groups = fpath.read().strip().split("\n")

    return groups
