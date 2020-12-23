import os
from collections import deque
from copy import deepcopy


def play_combat(players_cards, recursive=False):
    previous_p1, previous_p2 = [], []
    game_round = 0

    while players_cards["Player 1"] and players_cards["Player 2"]:
        # Check if current hand was already in previous hand
        if recursive:
            # Add to previous hands seen
            previous_p1.append(list(players_cards["Player 1"]))
            previous_p2.append(list(players_cards["Player 2"]))

            if game_round != 0:
                for hand in range(game_round):
                    if previous_p1[hand] == list(players_cards["Player 1"]) or\
                        previous_p2[hand] == \
                            list(players_cards["Player 2"]):

                        return "Player 1"
        # If both players draw the card value equal to number of cards, play
        # subgames
        if len(players_cards["Player 1"]) > players_cards["Player 1"][0] and \
                len(players_cards["Player 2"]) > players_cards["Player 2"][0]\
                and recursive:
            sub_game = deepcopy(players_cards)
            sub_game["Player 1"] = deque(list(sub_game["Player 1"])[
                                         1:sub_game["Player 1"][0] + 1])
            sub_game["Player 2"] = deque(list(sub_game["Player 2"])[
                                         1:sub_game["Player 2"][0] + 1])

            winner = play_combat(sub_game, recursive)

        # Normal game
        else:
            # P1 wins
            if players_cards["Player 1"][0] > players_cards["Player 2"][0]:
                winner = "Player 1"
            # P2 wins
            else:
                winner = "Player 2"

        # Cycle cards based on winner
        if winner == "Player 1":
            players_cards["Player 1"].append(
                players_cards["Player 1"].popleft())
            players_cards["Player 1"].append(
                players_cards["Player 2"].popleft())
        else:
            players_cards["Player 2"].append(
                players_cards["Player 2"].popleft())
            players_cards["Player 2"].append(
                players_cards["Player 1"].popleft())

        game_round += 1

    winner = "Player 1" if players_cards["Player 1"] else "Player 2"

    return winner


def sum_winner(players_cards, winner):
    winning_sum, multiplier = 0, 1

    players_cards[winner].reverse()
    for i in range(0, len(players_cards[winner])):
        winning_sum += multiplier * players_cards[winner][i]
        multiplier += 1

    return winning_sum


def main():
    players_cards = {}

    # User input
    players_file = input("Enter file containing player's and their cards: ")

    # Read input
    with open(os.path.realpath(players_file), "r") as in_file:
        players_file = in_file.read()
    players_file = players_file.rstrip().split("\n\n")

    # Identify players and their card
    players_file = [info.split(":\n") for info in players_file]
    for player in range(2):
        players_cards[players_file[player][0]] = \
            deque(map(int, players_file[player][1].split("\n")))

    # Create a copy with new memory address for part 2
    players_cards_combat = deepcopy(players_cards)

    # Part 1: Crab combat
    winner = play_combat(players_cards_combat)
    winning_sum = sum_winner(players_cards_combat, winner)
    print(f"The winner is {winner} with a winning sum of: {winning_sum}")

    # Part 2: Recursive combat
    winner = play_combat(players_cards, recursive=True)
    winning_sum = sum_winner(players_cards, winner)
    print(f"The winner is {winner} with a winning sum of: {winning_sum}")


if __name__ == '__main__':
    main()
