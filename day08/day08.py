import os


def action(k, val, accum, pointer):
    if k == "nop":
        pointer += 1
    elif k == "acc":
        accum += val
        pointer += 1
    else:
        pointer += val

    return accum, pointer


def calc_accum(k, val):
    pointer = 0
    accumulator = 0
    visited = {}
    status = False

    # Loop until encountering previosly visited pointer
    while pointer not in visited:
        visited[pointer] = True
        accumulator, pointer = action(
            k[pointer], val[pointer], accumulator, pointer)

        if pointer == len(k) - 1:
            status = True
        elif pointer >= len(k) - 1:
            break

    return status, accumulator, list(visited.keys())


def fix_bug(k, val, loop_mem):
    k = list(k)
    for i in range(len(loop_mem) - 1, 0, -1):
        # Check to see if key matches potential fixes, skip otherwise
        if k[loop_mem[i]] not in ["nop", "jmp"]:
            continue

        # Check potential fix
        k_new = k.copy()
        k_new[loop_mem[i]] = ["nop" if k[loop_mem[i]] == "jmp" else "jmp"][0]

        status, loop_accum, loop_mem = calc_accum(k_new, val)

        # If code loops properly, return fixed values
        if status:
            return status, loop_accum, loop_mem

    return status, loop_accum, loop_mem


def main():
    # Open instructions file
    instructions_file = input("Entire path containing instructions: ")

    with open(os.path.realpath(instructions_file), "r") as in_file:
        k, values = zip(*(instruction.split(" ") for instruction in in_file))

    values = [int(val.rstrip("\n")) for val in values]

    # Part 1
    status, loop_accum, loop_mem = calc_accum(k, values)
    print(f"The value of the accumulator before looping is: {loop_accum}")

    # Part 2
    status, loop_accum, loop_mem = (fix_bug(k, values, loop_mem))
    if status:
        print(
            f"The value of the accumulator of the fixed code is: {loop_accum}")
    else:
        print("Code is still looping infinitely")


if __name__ == "__main__":
    main()
