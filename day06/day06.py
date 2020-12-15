import os
from collections import Counter


def get_group(answers):
    group_size = [ans.rstrip("\n").count("\n") + 1 for ans in answers]
    group_answers = ["".join(ans.replace("\n", "")) for ans in answers]

    return group_size, group_answers


def count_consensus(group_answers, group_size):
    consensus_count = []
    for aidx, ans in enumerate(group_answers):
        unique_count = list(Counter(ans).values())
        consensus_count.append(unique_count.count(group_size[aidx]))

    return sum(consensus_count)


def count_unique(group_answers):
    count = sum(len(set(ans)) for ans in group_answers)

    return count


def main():
    answer_file = input("Enter path to file containing group answers: ")

    # Read file
    with open(os.path.realpath(answer_file), 'r') as in_file:
        answers = in_file.read()

    # Separate by empty line
    group_size, group_answers = get_group(answers.rsplit("\n\n"))

    # Part 1 - count number of unique yes within group
    unique_sum = count_unique(group_answers)
    print("Sum of counts is: {}".format(unique_sum))

    # Part 2 - count consensus yes
    consensus_sum = count_consensus(group_answers, group_size)
    print("Sum of consensus is {}".format(consensus_sum))


if __name__ == "__main__":
    main()
