"""
play using a pre-compiled strategy from the file "tree.pkl"
"""

import unittest
from random import choice
import pickle
import json
from sys import argv
from collections import Counter


with open("wordlist.txt") as f:
    wordlist = [line.strip() for line in f]

# with open("grades.json") as f:
#     grades = json.load(f)

# with open("tree.pkl", "rb") as f:
#     tree = pickle.load(f)



GRAY = 0
YELLOW = 1
GREEN = 2


class Grade(list):
    def __hash__(self):
        return sum(self[i] * 3**i for i in range(5))
            

def grade(guess, actual):
    """
    Return 5 values from (GRAY, YELLOW, GREEN)
    """
    # everything defaults to gray
    result = Grade([GRAY, GRAY, GRAY, GRAY, GRAY])

    actual_counts = Counter(actual)
    
    # for each letter that's in the right spot: assign green
    for i in range(5):
        guess_char = guess[i]
        actual_char = actual[i]
        if guess_char == actual_char:
            result[i] = GREEN
            actual_counts[actual_char] -= 1

    # now for the non-green guess letters, if there's a different spot where it
    # would match, make it yellow *but* count how many of each letter has been
    # used.
    for i in range(5):
        guess_char = guess[i]
        actual_char = actual[i]

        # if this letter was an exact match, it's already marked green
        if guess_char == actual_char:
            continue

        if actual_counts[guess_char] > 0:
            result[i] = YELLOW
            actual_counts[guess_char] -= 1
        else:
            result[i] = GRAY

    return result


def play_wordle(solution, tree):
    subtree = tree
    guesses = []
    while subtree[1] != {"242": None}:
        # use this guess and get the next subtree
        guess, outcomes = subtree
        guesses.append(guess)
        this_grade = grade(guess, solution)
        subtree = outcomes[str(hash(this_grade))]

    if subtree[0] not in guesses:
        guesses.append(subtree[0])

    return guesses


if __name__ == "__main__":
    with open("strategy_expected.json") as f:
        tree = json.load(f)

    if len(argv) == 2:
        print(play_wordle(argv[1], tree))

    histogram = [0 for _ in range(10)]
    double_histogram = [0 for _ in range(10)]
    for word in wordlist:
        count = len(play_wordle(word, tree))
        if len(set(word)) == 5:
            histogram[count] += 1
        else:
            double_histogram[count] += 1

    print("no doubles:")
    print(histogram)
    print(f"(average = {sum(i * x for i, x in enumerate(histogram)) / sum(histogram)})")
    print()
    print("doubles:")
    print(double_histogram)
    print(f"(average = {sum(i * x for i, x in enumerate(double_histogram)) / sum(double_histogram)})")
