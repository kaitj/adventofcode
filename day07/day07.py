import os
import re
from collections import defaultdict

def parse_relationship(rules, bag_map):
    for rule in rules.split("\n"):
        # Identify parent vs child bags
        content_re = re.match(r"([a-zA-Z ]+) bags contain ((?:\d+ [a-zA-Z ]+ bags?(?:, )?)+)\.", rule)
        if content_re == None:
            continue
        main_bag, bag_contents = content_re.groups()

        # Identify number of child bags and colours
        bag_contents = bag_contents.split(", ")
        bag_contents = [re.match(r"(\d+) ([a-zA-Z ]+) bags?", content).groups() for content in bag_contents]
        
        # Store relationships
        for content in bag_contents:
            bag_map[main_bag]["contain"].append(content)
            bag_map[content[1]]["contained by"].append((int(content[0]), main_bag))

def find_bag_parent(bag_map, bag_colour, main_bag_colour):
    for parent in bag_map[bag_colour]["contained by"]:
        main_bag_colour.add(parent[1])
        if len(bag_map[parent[1]]["contained by"]) > 0:
            find_bag_parent(bag_map, parent[1], main_bag_colour)

def find_bag_child(bag_map, bag_colour, num_bags=0):
    for child in bag_map[bag_colour]["contain"]:
        num_bags += int(child[0])  
        num_bags += int(child[0]) * find_bag_child(bag_map, child[1])

    return num_bags


if __name__ == "__main__":
    rules_file = "input.txt"

    # Read entire rules file 
    with open(os.path.realpath(rules_file), "r") as f:
        bag_rules = f.read()

    # Identify rules
    bag_map = defaultdict(lambda: defaultdict(list))
    parse_relationship(bag_rules, bag_map)

    # Identify number of potential shiny gold bags
    gold_parents = set()
    find_bag_parent(bag_map, "shiny gold", gold_parents)

    # Identify possible number of child bags
    gold_children = find_bag_child(bag_map, "shiny gold")

    # Answers
    print(f"Number of potential bags able to hold shiny gold bags: {len(gold_parents)}")
    print(f"Number of potential children bags: {gold_children}")