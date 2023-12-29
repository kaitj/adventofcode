from collections import defaultdict
from pathlib import Path

NEIGHBORS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]
PADDING = 2


def get_picture(raw_pic: str) -> dict[tuple[int, int], int]:
    picture: dict[tuple[int, int], int] = defaultdict(int)
    for idx in range(len(raw_pic)):
        for jdx in range(len(raw_pic[0])):
            picture[(idx, jdx)] = 1 if raw_pic[idx][jdx] == "#" else 0
    return picture


def decode_pixel(position: int, codec: str):
    return 1 if codec[position] == "#" else 0


def parse_input(in_fpath: Path) -> tuple[str, dict[tuple[int, int], int]]:
    with in_fpath.open() as in_file:
        raw_data = in_file.read().split("\n\n")
    codec = "".join(raw_data[0].splitlines())
    pic = get_picture(raw_data[1].splitlines())  # type: ignore

    return codec, pic


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    codec, pic = parse_input(in_fpath)
    steps = 50
    values = []

    for tick in range(1, steps + 1):
        new_pic = defaultdict(int)

        min_i, min_j, max_i, max_j = None, None, None, None

        for pixel in pic:
            i, j = pixel[0], pixel[1]
            if min_i is None or i < min_i:
                min_i = i
            if min_j is None or j < min_j:
                min_j = j
            if max_i is None or i > max_i:
                max_i = i
            if max_j is None or j > max_j:
                max_j = j

        for i in range(min_i - PADDING, max_i + PADDING):
            for j in range(min_j - PADDING, max_j + PADDING):
                current = (i, j)
                position = ""

                for offset in NEIGHBORS:
                    neighbour = (current[0] + offset[0], current[1] + offset[1])
                    px = pic.get(neighbour, 0 if tick % 2 else 1)
                    position += str(px)
                position = int(position, 2)
                new_pic[(i, j)] = decode_pixel(position, codec)
        pic = new_pic

        if tick == 2 or tick == 50:
            values.append(sum(pic.values()))

    print(f"Answer: {values[0]}")
    print(f"Answer: {values[-1]}")
