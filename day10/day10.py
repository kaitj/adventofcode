import os
import operator
from collections import Counter, deque

def compute_diff(adapter_list):
    adapter_diff = list(map(operator.sub, adapter_list[1:], adapter_list[:-1]))
    adapter_diff = Counter(adapter_diff)
    adapter_diff = adapter_diff[1] * adapter_diff[3]

    return adapter_diff

def compute_chains(adapter_list):
    # Dict to store routes, initialize path to start
    chains = {}
    chains[0] = 1
    for a in adapter_list[1:]:
        chains[a] = chains.get(a-1,0) + chains.get(a-2,0) + chains.get(a-3,0)

    adapter_combos = chains[adapter_list[-1]]

    return adapter_combos


def main():
    # Read adapter file 
    adapter_file = input("Enter file containing adapter list: ")

    with open(os.path.realpath(adapter_file), "r") as f:
        adapter_list = f.read().split()
    adapter_list = deque(sorted(map(int, adapter_list)))

    # Add charging outlet and built-in adapter
    adapter_list.appendleft(0)
    adapter_list.append(max(adapter_list)+3)
    adapter_list = list(adapter_list)

    # Compute adapter difference and multiple 1- & 3- jolt difference
    adapter_mult = compute_diff(adapter_list)
    print(f"The multiplication of 1-jolt & 3-jolt differences is: {adapter_mult}")

    # Computer number of chains
    adapter_combos = compute_chains(adapter_list)
    print(f"The number of possible adapter chains: {adapter_combos}")


if __name__ == "__main__":
    main()