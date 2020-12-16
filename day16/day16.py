import os
import re
import operator
from functools import reduce
from collections import defaultdict


def extract_rules(content):
    rules = defaultdict(list)

    # Use regex to find rules
    rules_reg = r"([\w\s]+):\s(\d+-\d+)\s\w+\s(\d+-\d+)*"
    groups = re.findall(rules_reg, content)

    for group in groups:
        rules[group[0]].append(list(map(int, group[1].split("-"))))
        rules[group[0]].append(list(map(int, group[2].split("-"))))

    return rules


def check_bounds(value, bounds):
    return value in range(bounds[0][0], bounds[0][1] + 1) or \
        value in range(bounds[1][0], bounds[1][1] + 1)


def find_invalid(rules, tickets):
    invalid_num, invalid_tickets = [], []

    for ticket_id, ticket in enumerate(tickets):
        for num in ticket:
            validity = [check_bounds(num, rules[key]) for key in rules.keys()]

            if not any(validity):
                invalid_num.append(num)
                invalid_tickets.append(ticket_id)

    valid_tickets = [ticket for ticket_id, ticket in enumerate(
        tickets) if ticket_id not in invalid_tickets]

    return invalid_num, valid_tickets


def identify_fields(rules, valid_tickets, keyword):
    ticket_fields = defaultdict(set)

    # Identify potential fields for each position
    for num_id in range(len(valid_tickets[0])):
        possible_fields = set(rules.keys())
        for ticket in valid_tickets:
            possible_fields = possible_fields & set(
                key for key in rules.keys() if check_bounds(
                    ticket[num_id], rules[key]))

        ticket_fields[num_id] = possible_fields

    # Identify field positions
    fields_found, fields_idx = [], []
    while len(fields_found) < len(ticket_fields):
        for position, fields in ticket_fields.items():
            if len(fields) == 1:
                fields_found.append(fields.pop())
                fields_idx.append(position)
            else:
                ticket_fields[position] = ticket_fields[position] - \
                    set(fields_found)

    fields_found = [fields_idx[idx] for idx, field in enumerate(
        fields_found) if field.strip().startswith(keyword)]

    return fields_found


def main():
    ticket_file = input("Enter the file containing ticket translation info: ")

    with open(os.path.realpath(ticket_file), "r") as in_file:
        file_content = in_file.read()
    file_content = file_content.rsplit("\n\n")
    file_content = [content.replace("\n", " ") for content in file_content]

    # Store file contents
    rules = extract_rules(file_content[0])
    your_ticket = list(map(int, file_content[1].split(": ")[1].split(",")))
    nearby_tickets = file_content[2].split(
        ": ")[1].replace(" ", "\n").split("\n")
    nearby_tickets = [list(map(int, ticket.split(",")))
                      for ticket in nearby_tickets]

    # Part 1: Find invalid nearby tickets
    invalid_num, valid_tickets = find_invalid(rules, nearby_tickets)
    print(f"Number of invalid tickets: {sum(invalid_num)}")

    # Part 2: Find fields
    fields_found = identify_fields(rules, valid_tickets, "departure")
    ticket_mul = reduce(
        operator.mul, [
            your_ticket[pos] for pos in fields_found])
    print(f"Product of departure fields is: {ticket_mul}")


if __name__ == "__main__":
    main()
