#!/usr/bin/env python
import time
import urllib.error
import urllib.parse
import urllib.request
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import date
from pathlib import Path

from aoc.utils import TOP_DIR, get_cookie_headers, shell


def get_input(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    req = urllib.request.Request(url, headers=get_cookie_headers())
    return urllib.request.urlopen(req).read().decode()


def download_input(year: int, day: int, input_path: Path) -> int:
    for _ in range(5):
        try:
            input_content = get_input(year=year, day=day)
        except urllib.error.URLError as err:
            print(f"Not ready yet: {err}")
            time.sleep(1)
        else:
            break
    else:
        raise SystemExit("Timed out after many attempts")

    with input_path.open(mode="w") as input_file:
        input_file.write(input_content)

    return 0


def init_day():
    # Get arguments
    parser = ArgumentParser(
        description="Helper script to initialize each day of advent of code",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "day",
        type=int,
        choices=range(1, 26),
        metavar="[1-25]",
        help="Day of advent of code to setup",
    )
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=int(date.today().year),
        dest="year",
        action="store",
    )
    args = parser.parse_args()

    day = f"day{args.day:02d}"
    year = args.year

    # git commands
    shell("git checkout main")
    shell("git pull -r origin main")
    shell('git branch --merged | egrep -v "(^\\*|main)" | xargs git branch -d ")')
    shell(f"git checkout -B {year}/{day}")

    # Update template for current day
    day_dir = Path(TOP_DIR).joinpath(day)
    day_dir.mkdir(parents=True, exist_ok=True)

    with TOP_DIR.joinpath("day00/day00.py").open(encoding="utf-8") as tpl_file:
        content = tpl_file.read()
    content = content.replace("Day00", f"{day.capitalize()}")
    with day_dir.joinpath(f"{day}.py").open(mode="w", encoding="utf-8") as out_file:
        out_file.write(content)

    # Get remote content
    download_input(
        year=year, day=int(day[3:]), input_path=day_dir.joinpath("input.txt")
    )
    shell(f"touch {day_dir.joinpath('test_input_part1.txt')}")
    shell(f"touch {day_dir.joinpath('test_input_part2.txt')}")
