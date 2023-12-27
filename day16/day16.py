from functools import reduce
from pathlib import Path
from typing import Self


def parse_input(in_fpath: Path) -> str:
    with in_fpath.open() as in_file:
        content = in_file.read().strip()

    return content


class Bitstream:
    def __init__(self: Self, hexstream: str):
        self.bitstream: list[str] = []
        for c in hexstream:
            self.bitstream.extend(bin(int(c, 16))[2:].zfill(4))
        # number of bits read overall
        self.read = 0
        # sum of all versions
        self.versionsum = 0

    def get_bits(self: Self, n: int):
        self.read += n
        bits = self.bitstream[:n]
        self.bitstream = self.bitstream[n:]
        return bits

    def decode_bits(self: Self, x: list[str]):
        return int("".join([str(b) for b in x]), 2)

    def get_literal(self):
        number: list[str] = []
        while True:
            last = self.decode_bits(self.get_bits(1)) == 0
            number.extend(self.get_bits(4))
            if last:
                break
        return self.decode_bits(number)

    def decode_packet(self: Self) -> int:
        version = self.decode_bits(self.get_bits(3))
        id = self.decode_bits(self.get_bits(3))
        self.versionsum += version

        if id == 4:  # literal packet
            value = self.get_literal()
        else:  # operator packet
            lengthtype = self.decode_bits(self.get_bits(1))
            v: list[int] = []  # collect all literals
            if lengthtype == 0:  # bit length
                length = self.decode_bits(self.get_bits(15))
                pos = self.read
                while pos + length > self.read:
                    v.append(self.decode_packet())
            elif lengthtype == 1:  # number of subpackets
                subpackets = self.decode_bits(self.get_bits(11))
                for _ in range(subpackets):
                    v.append(self.decode_packet())
            else:
                raise ValueError(f"Unknown length type: {lengthtype}")

            if id == 0:  # +
                value = sum(v)
            elif id == 1:  # *
                value = reduce(lambda x, y: x * y, v)
            elif id == 2:  # min
                value = min(v)
            elif id == 3:  # max
                value = max(v)
            elif id == 5:  # >
                value = int(v[0] > v[1])
            elif id == 6:  # <
                value = int(v[0] < v[1])
            elif id == 7:  # ==
                value = int(v[0] == v[1])
            else:
                raise ValueError(f"Unknown operator: {id}")
        return value


if __name__ == "__main__":
    in_fpath = Path(__file__).parent.joinpath("input.txt")
    content = parse_input(in_fpath)
    bs = Bitstream(content)
    res = bs.decode_packet()

    print(f"Answer: {bs.versionsum}")
    print(f"Answer: {res}")
