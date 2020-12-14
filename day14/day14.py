import os
from collections import defaultdict
from itertools import product

def apply_mask(mask, value):
    # Apply mask to binary string
    mask_idx = [idx for idx, m in enumerate(mask) if m != "X"]

    for m in mask_idx: 
        if mask[m] == "1":
            value = value[:m] + str(int(value[m]) | int(mask[m])) + value[m+1:]
        else:
            value = value[:m] + "0" + value[m+1:]
    
    return int(value, 2)

def decoder(init_prog, version):
    # Memory dictionary
    mem = {}

    for task, value in init_prog:
        if task == "mask":
            mask = value
        elif task.find("mem") >= 0:
            addr = int(task[4:-1])
            value = format(int(value), "036b")
            
            if version == 1:
                mem[addr] = apply_mask(mask, value)
            else:
                addr_list = update_addr(mask, addr)
                for addr in addr_list:
                    mem[addr] = int(value, 2)

    return mem

def update_addr(mask, addr):
    addr_bit = format(int(addr), "036b")

    change_bit = {"0": lambda val: str(val),
                  "1": lambda val: "1",
                  "X": lambda val: "X",
    }

    # Get updated mask from address
    new_addr = "".join(change_bit[mask[m]](addr_bit[m]) for m in range(len(mask)))
    addr_list = []

    addr_idx = [idx for idx, m in enumerate(new_addr) if m == "X"]

    # Get all possible combinations of masks
    for bit_replacement in product(range(2), repeat=len(addr_idx)):
        addr_combo = list(new_addr)
        for b, bit in enumerate(bit_replacement):
            addr_combo[addr_idx[b]] = str(bit)
        addr_list.append("".join(addr_combo))

    return addr_list

def sum_mem(mem):
    return sum(mem.values())

def main():
    init_file = input("Entire file containing initialization program: ")

    with open(os.path.realpath(init_file), "r") as f:
        init_prog = [l.strip().split(" = ") for l in f]

    # Part 1 
    mem_v1 = decoder(init_prog, 1)
    print(f"Sum of values left in memory: {sum_mem(mem_v1)}")

    # Part 2 
    mem_v2 = decoder(init_prog, 2)  
    print(f"Sum of values left in memory: {sum_mem(mem_v2)}") 

if __name__ == "__main__":
    main()