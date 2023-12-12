#!/usr/bin/env python
import subprocess
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import date
from pathlib import Path

YEAR = str(date.today().year)
DAY = f"day{date.today().day:02d}"
TOP_DIR = Path(__file__).parent.parent


def shell(cmd: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(cmd, shell=True)


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Helper script to help setup each day of advent of code",
        formatter_class=RawTextHelpFormatter,
    )

    # Required arguments
    parser.add_argument(
        "day",
        default=00,
        type=int,
        help="Current day of advent of code",
    )

    # Version (year)
    parser.add_argument(
        "-v",
        "--version",
        dest="version",
        action="version",
        version=str(YEAR),
    )

    return parser


def main():
    # Get arguments
    args = get_parser().parse_args()

    if not isinstance(args.day, int):
        raise TypeError("Day should be provided as an integer (e.g. 1, 2, 10, etc)")
    DAY = f"day{args.day:02d}"

    # git commands
    shell("git checkout main")
    shell("git pull -r origin main")
    shell(f"git checkout -b {YEAR}/{DAY}")

    # Update template for current day
    day_dir = Path(TOP_DIR).joinpath(DAY)
    day_dir.mkdir(parents=True, exist_ok=True)

    with TOP_DIR.joinpath("day00/day00.py").open(encoding="utf-8") as tpl_file:
        content = tpl_file.read()
    content = content.replace("day00", f"{DAY}")
    with day_dir.joinpath(f"{DAY}.py").open(mode="w", encoding="utf-8") as out_file:
        out_file.write(content)

    # Get remote content
    shell(f"touch {day_dir.joinpath('input.txt')}")
    shell(f"touch {day_dir.joinpath('test_input_part1.txt')}")
    shell(f"touch {day_dir.joinpath('test_input_part2.txt')}")
