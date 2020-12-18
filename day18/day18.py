import os
import re
from functools import partial


def simple_math(line):
    """ Function to evaluate math expression given new ordering rules """
    math_pattern = re.compile(r"\d+\s*[*+]\s*\d+")

    while not line.isdigit():
        line = math_pattern.sub(lambda x: str(eval(x.group())), line, count=1)

    return int(line)


def adv_math(line):
    """ Function to evaluate math expression given addition before
        multiplication """
    add_pattern = re.compile(r"\d+\s*[+]\s*\d+")
    mul_pattern = re.compile(r"\d+\s*[*]\s*\d+")

    # Evaluate addition before multiplication
    while "+" in line:
        line = add_pattern.sub(lambda x: str(eval(x.group())), line)
    while "*" in line:
        line = mul_pattern.sub(lambda x: str(eval(x.group())), line)

    return int(line)


def proc_parentheses(line, part=None):
    """ Evaluate parentheses first, but as separate computation """
    line = line.group()

    if line[0] == "(":
        line = line[1:-1]

    return str(part(line))


def eval_expr(line, part):
    """ Evaluate full math expression """
    chunk = partial(proc_parentheses, part=part)
    while "(" in line:
        line = re.sub(r"\([^()]+\)", chunk, line)

    return part(line)


def main():
    math_file = input("Enter the file containing the math homework: ")

    with open(os.path.realpath(math_file), "r") as in_file:
        hw_lines = in_file.read()

    p1_sum = p2_sum = 0
    for line in hw_lines.rsplit("\n"):
        p1_sum += eval_expr(line, simple_math)
        p2_sum += eval_expr(line, adv_math)

    print(f"The sum of all values of the homework is: {p1_sum}")
    print(f"The sum of all values of the homework is: {p2_sum}")


if __name__ == '__main__':
    main()
