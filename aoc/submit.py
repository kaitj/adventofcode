import re
import urllib.error
import urllib.parse
import urllib.request
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import date

from aoc.utils import TOP_DIR, get_cookie_headers, shell

TOO_QUICK = re.compile("You gave an answer too recently.*to wait.")
WRONG = re.compile(r"That's not the right answer.*?\.")
RIGHT = "That's the right answer!"
ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")


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


def run_test(day: int, part: int) -> None:
    day_fpath = TOP_DIR.joinpath(f"day{day:02d}/day{day:02d}.py")
    shell(f"pytest {day_fpath} -k part{part} -s --pdb")


def run_day(day: int, part: int) -> int:
    day_fpath = TOP_DIR.joinpath(f"day{day:02d}/day{day:02d}.py")
    answer = shell(
        f"python {day_fpath} -p {part}",
        capture_output=True,
    )

    if answer.stderr:
        msg = answer.stderr.decode("utf-8")
        raise Exception(msg)

    return int(answer.stdout.strip())


def submit_solution() -> int:
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
    parser.add_argument("-t", "--test", default=False, dest="test", action="store_true")
    parser.add_argument(
        "-n", "--dry-run", default=False, dest="dry_run", action="store_true"
    )
    args = parser.parse_args()

    if args.test:
        run_test(day=args.day, part=args.part)
        return 0

    answer = run_day(day=args.day, part=args.part)
    print(f"Answer: {answer}")

    if not (args.dry_run):
        contents = _post_answer(
            year=args.year, day=args.day, part=args.part, answer=answer
        )

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
    else:
        print("\nDry-run/test, answer not submitted.")
        return 0
