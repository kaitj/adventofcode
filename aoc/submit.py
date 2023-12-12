import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import date

from aoc.utils import get_cookie_headers


def _post_answer(year: int, day: int, part: int, answer: int) -> str:
    params = urllib.parse.urlencode({"level": part, "answer": answer})
    req = urllib.request.Request(
        f"https://adventofcode.com/{year}/day/{day}/answer",
        method="POST",
        data=params.encode(),
        headers=get_cookie_headers(),
    )
    resp = urllib.request.urlopen(req)

    return resp.read().decode()


def submit_solution() -> int:
    TOO_QUICK = re.compile("You gave an answer too recently.*to wait.")
    WRONG = re.compile(r"That's not the right answer.*?\.")
    RIGHT = "That's the right answer!"
    ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")

    parser = ArgumentParser(
        description="Helper script to submit solution to advent of code",
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
    parser.add_argument(
        "-p",
        "--part",
        type=int,
        choices=[1, 2],
        default=1,
        dest="part",
        action="store",
    )
    args = parser.parse_args()

    year, day = args.year, args.day
    answer = int(sys.stdin.read())

    print(f"Answer: {answer}")

    contents = _post_answer(year=year, day=day, part=args.part, answer=answer)

    for error_regex in (WRONG, TOO_QUICK, ALREADY_DONE):
        error_match = error_regex.search(contents)
        if error_match:
            print(f"\033[41m{error_match[0]}\033[m")
            return 1

    if RIGHT in contents:
        print(f"\033[42m{RIGHT}\033[m")
        return 0
    else:
        # Unexpected output
        print(contents)
        return 1
