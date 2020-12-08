import os 

def action(k, v, accum, pointer):
    if k == "nop":
        pointer += 1
    elif k == "acc":
        accum += v
        pointer += 1
    else:
        pointer += v

    return accum, pointer

def calc_accum(k, v):
    pointer = 0
    accumulator = 0
    visited = {}
    status = False

    # Loop until encountering previosly visited pointer
    while pointer not in visited:
        visited[pointer] = True
        accumulator, pointer = action(k[pointer], v[pointer], accumulator, pointer)

        if pointer == len(k)-1:
            status = True
        elif pointer >= len(k)-1:
            break
            
    return status, accumulator, list(visited.keys())

def fix_bug(k, v, loop_mem):
    k = list(k)
    for i in range(len(loop_mem)-1, 0, -1):
        # Check to see if key matches potential fixes, skip otherwise
        if k[loop_mem[i]] not in ["nop", "jmp"]:
            continue
        
        # Check potential fix
        k_new = k.copy()
        k_new[loop_mem[i]] = ["nop" if k[loop_mem[i]] == "jmp" else "jmp"][0]

        status, loop_accum, loop_mem = calc_accum(k_new, v)

        # If code loops properly, return fixed values
        if status == True:
            return status, loop_accum, loop_mem
    
    return status, loop_accum, loop_mem
    

def main():
    # Open instructions file 
    instructions_file = input("Entire path containing instructions: ")

    with open(os.path.realpath(instructions_file), "r") as f:
        k, v = zip(*(instruction.split(" ") for instruction in f))
    
    v = [int(val.rstrip("\n")) for val in v]

    # Part 1 
    status, loop_accum, loop_mem = calc_accum(k,v)
    print(f"The value of the accumulator before looping is: {loop_accum}")

    # Part 2
    status, loop_accum, loop_mem = (fix_bug(k, v, loop_mem))
    if status == True:
        print(f"The value of the accumulator of the fixed code is: {loop_accum}")
    else:
        print(f"Code is still looping infinitely")

if __name__ == "__main__":
    main()