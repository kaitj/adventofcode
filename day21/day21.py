import os
from collections import defaultdict


def identify_allergens(foods):
    foreign_ingredient, known_allergens = defaultdict(int), {}

    for food in foods:
        # Identify ingredients
        for ingredient in food[0]:
            foreign_ingredient[ingredient] += 1
        # Identify allergens
        for allergen in food[1]:
            if allergen not in known_allergens:
                known_allergens[allergen] = set(food[0])
            else:
                known_allergens[allergen] = set(
                    known_allergens[allergen]) & set(
                    food[0])

    # Get set of allergens from dictionary
    potential_allergens = set()
    for allergen in known_allergens:
        potential_allergens = potential_allergens | known_allergens[allergen]

    # Count non allergens
    good_count = sum([foreign_ingredient[food]
                      for food in foreign_ingredient
                      if food not in potential_allergens])

    # Associate allergens with ingredients
    food_found, ingredients = [], []
    while len(food_found) < len(known_allergens):
        for key, allergen in known_allergens.items():
            if len(allergen) == 1:
                food_found.append(key)
                ingredients.append(allergen.pop())
            else:
                known_allergens[key] = known_allergens[key] - set(ingredients)

    allergens = ",".join(
        [ingredient for _, ingredient in sorted(zip(food_found, ingredients))])

    return good_count, allergens


def main():
    # User input
    in_file = input("Enter file containing ingredients list: ")

    with open(os.path.realpath(in_file), "r") as food_file:
        foods = [food.strip("\n)").split(" (contains ") for food in food_file]

    # Split ingredients from allergens
    for food in foods:
        food[0] = food[0].split(" ")
        food[1] = food[1].split(", ")

    good_count, allergens = identify_allergens(foods)
    # Part 1
    print(f"Number of non-allergen ingredients: {good_count}")
    # Part 2
    print(f"Canonical dangerous ingredients list: {allergens}")


if __name__ == '__main__':
    main()
