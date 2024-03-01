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
    with open("strategy.json") as f:
        tree = json.load(f)

    # if there is an argument, play wordle with it. Otherwise play all possible
    # games and show statistics
    if len(argv) == 2:
        guesses = play_wordle(argv[1], tree)
        print(f"guesses: {', '.join(guesses)}")
    else:
        histogram = [0 for _ in range(10)]
        lost_words = []
        for word in wordlist:
            count = len(play_wordle(word, tree))
            histogram[count] += 1
            if count > 6:
                lost_words.append(word)

        max_guesses = max(i for i, count in enumerate(histogram) if count > 0)
        print(f"Out of {len(wordlist)} games:")
        for count in range(1, max_guesses + 1):
            print(f"{count} guesses: {histogram[count]} games")
        print()

        average = sum(i * count for i, count in enumerate(histogram)) / sum(histogram)
        print(f"average guesses: {average}")
        print()

        won = sum(count for i, count in enumerate(histogram) if i <= 6)
        print(f"won {won} / {len(wordlist)} games")
        print()

        print(f"failed for words {', '.join(lost_words)}")
