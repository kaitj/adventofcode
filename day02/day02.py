import utils


def parse_pair(pair, x, y, aim=None):
    key, val = pair.split(" ")[0], int(pair.split(" ")[1])

    if aim is not None:
        match key:
            case "down":
                return x, y, aim + val
            case "up":
                return x, y, aim - val
            case "forward":
                return x + val, y + (aim * val), aim
    else:
        match key:
            case "forward":
                return x + val, y, aim
            case "up":
                return x, y - val, aim
            case "down":
                return x, y + val, aim


def planned_course(groups, aim=None):
    x, y = 0, 0

    for pair in groups:
        x, y, aim = parse_pair(pair, x, y, aim)
    
    return x, y


if __name__ == "__main__":
    input_fpath = input("Enter path containing input commands: ")
    in_cmds = utils.parse_group(input_fpath)

    # Puzzle 1
    x_pos, y_pos = planned_course(in_cmds)
    print(f"1. Depth x position = {x_pos * y_pos}")

    # Puzzle 2
    x_pos, y_pos = planned_course(in_cmds, aim=0)
    print(f"2. Depth * position = {x_pos * y_pos}")
