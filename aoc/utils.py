#!/usr/bin/env python
import subprocess
from argparse import ArgumentParser
from pathlib import Path

TOP_DIR = Path(__file__).parent.parent


def shell(cmd: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(cmd, shell=True)


def get_cookie_headers() -> dict[str, str]:
    # Note: Cookie file (.cookie) may need to be updated with "session=" prefix
    with TOP_DIR.joinpath(".cookie").open() as in_file:
        contents = in_file.read().strip()
    return {"Cookie": contents, "User-Agent": "kaitj"}


def day_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "-p",
        "--part",
        type=int,
        choices=[1, 2],
        default=1,
        dest="part",
        action="store",
    )

    return parser
