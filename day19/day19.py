import os
import re


def extract_rules(all_rules):
    rules = {}

    all_rules = all_rules.split("\n")

    for rule in all_rules:
        key, rule = rule.split(": ")
        rules[int(key)] = rule.replace('"', "")

    return rules


def match_message(rules, messages, part2=False):
    # Create regex pattern based on rules
    def expand(character):
        return rule_regex(int(character)) if character.isdigit() else character

    def rule_regex(key):
        return r"(?:" + "".join(map(expand, rules[key].split())) + ")"

    valid_matches = 0

    # Regex
    reg_message = rule_regex(0)
    if part2:
        reg_message = "(" + rule_regex(42) + "+)(" + rule_regex(31) + "+)"

    # Check messages for matches
    for message in messages:
        reg_match = re.fullmatch(reg_message, message)
        # If match found (part 1), increment counter
        if reg_match and not part2:
            valid_matches += 1
        # Else count if rule 42 > rule 31
        elif reg_match and len(reg_match.group(1)) > len(reg_match.group(2)):
            valid_matches += 1

    return valid_matches


def main():
    # User input
    rules_file = input("Enter file containing rules and messages: ")

    # Extract rules and messages
    with open(os.path.realpath(rules_file), "r") as in_file:
        content = in_file.read()
    rules, messages = content.rsplit("\n\n")
    rules = extract_rules(rules)
    messages = messages.split("\n")

    # Part 1: Identify valid messages and see it exists in messages list
    valid_p1 = match_message(rules, messages)
    print(f"Number of valid messages: {valid_p1}")

    # Part 2:
    valid_p2 = match_message(rules, messages, part2=True)
    print(f"Number of valid messages: {valid_p2}")


if __name__ == "__main__":
    main()
