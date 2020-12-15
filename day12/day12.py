import os


def navigate(instructions, waypoint=False):
    directions = {"N": (0, 1),
                  "S": (0, -1),
                  "E": (1, 0),
                  "W": (-1, 0)
                  }

    # Initialize variables
    xdir = ydir = 0
    dxdir, dydir = directions["E"] if not waypoint else (10, 1)

    # Follow instructions
    for inst, value in instructions:
        if inst == "L":
            for _ in range(value // 90):
                dxdir, dydir = -dydir, dxdir
        elif inst == "R":
            for _ in range(value // 90):
                dxdir, dydir = dydir, -dxdir
        elif inst == "F":
            xdir += dxdir * value
            ydir += dydir * value
        else:
            wdx, wdy = directions[inst]
            # Move waypoint
            if waypoint:
                dxdir += wdx * value
                dydir += wdy * value
            else:
                xdir += wdx * value
                ydir += wdy * value

    return abs(xdir) + abs(ydir)


def main():
    # Read directions from input file
    instructions_file = input("Enter file containing instructions: ")

    with open(os.path.realpath(instructions_file), "r") as in_file:
        instructions = [(d[0], int(d[1:].strip())) for d in in_file]

    # Part 1
    man_distance1 = navigate(instructions, False)
    print(
        f"The Manhattan distance between current and starting location is: {man_distance1}")

    # Part 2
    man_distance2 = navigate(instructions, True)
    print(
        f"The Manhattan distance, considering the waypoint is: {man_distance2}")


if __name__ == "__main__":
    main()
