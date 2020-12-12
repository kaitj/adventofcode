import os 

def navigate(instructions, waypoint=False):
    DIRECTIONS = {"N": (0, 1),
                  "S": (0, -1),
                  "E": (1, 0),
                  "W": (-1, 0)
    }

    # Initialize variables
    x = y = 0
    dx, dy = DIRECTIONS["E"] if not waypoint else (10, 1)

    # Follow instructions
    for inst, value in instructions:
        if inst == "L":
            for _ in range(value // 90):
                dx, dy = -dy, dx
        elif inst == "R":
            for _ in range(value // 90):
                dx, dy = dy, -dx
        elif inst == "F":
            x += dx * value
            y += dy * value
        else:
            wdx, wdy = DIRECTIONS[inst]
            # Move waypoint
            if waypoint:
                dx += wdx * value
                dy += wdy * value
            else:
                x += wdx * value
                y += wdy * value

    return abs(x) + abs(y)    

def main():
    # Read directions from input file
    instructions_file = input("Enter file containing instructions: ")

    with open(os.path.realpath(instructions_file), "r") as f:
        instructions = [(d[0], int(d[1:].strip())) for d in f]

    # Part 1
    man_distance1 = navigate(instructions, False)
    print(f"The Manhattan distance between current and starting location is: {man_distance1}")

    # Part 2
    man_distance2 = navigate(instructions, True)
    print(f"The Manhattan distance, considering the waypoint is: {man_distance2}")


if __name__ == "__main__":
    main()