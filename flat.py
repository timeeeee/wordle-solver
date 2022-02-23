from collections import defaultdict, Counter
from string import ascii_lowercase
import unittest
from copy import deepcopy
from random import choice, randint
import json


with open("wordlist.txt") as f:
    wordlist = [line.strip() for line in f]


GRAY = 0
YELLOW = 1
GREEN = 2

with open("grades.json") as f:
    grades = json.load(f)

def grade(guess, actual):
    """
    Return 5 values from (GRAY, YELLOW, GREEN)
    """
    # everything defaults to gray
    result = [GRAY, GRAY, GRAY, GRAY, GRAY]

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

class TestGrade(unittest.TestCase):
    def test_abyss_booby(self):
        self.assertListEqual(grade("abyss", "booby"), [GRAY, YELLOW, YELLOW, GRAY, GRAY])

    def test_booby_abyss(self):
        self.assertListEqual(grade("booby", "abyss"), [YELLOW, GRAY, GRAY, GRAY, YELLOW])

    def test_sissy_essay(self):
        self.assertListEqual(grade("sissy", "essay"), [YELLOW, GRAY, GREEN, GRAY, GREEN])

    def test_essay_sissy(self):
        self.assertListEqual(grade("essay", "sissy"), [GRAY, YELLOW, GREEN, GRAY, GREEN])

        

"""
class Hint(object):
    def __init__(self):
        # the letters that are allowed in each spot
        self.available_letters = [set(ascii_lowercase) for _ in range(5)]

        # Any time we get n yellow or green we have at least n of that letter
        self.min_counts = {char: 0 for char in ascii_lowercase}

        # if we get yellows or greens for a letter *and* at least one gray, we
        # know exactly how many of them to include in the solution
        self.exact_counts = dict()

    def is_valid(self, word):
        for char, allowed in zip(word, self.available_letters):
            if char not in allowed:
                return False

        counts = Counter(word)
        for char, min_count in self.min_counts.items():
            if counts[char] < min_count:
                return False

        for char, count in counts.items():
            if char in self.exact_counts:
                if self.exact_counts[char] != count:
                    return False

        return True

    def __eq__(self, other):
        pass

    def add_guess(self, guess, actual):
        hint = deepcopy(self)

        # for each spot, check and see if we have definitely the right or wrong letter
        for index, char in enumerate(guess):
            if char == actual[i]:
                hint.available_letters[i] = set([char])
            else:
                hint.available_letters[i].discard(char)

        # for each letter, do we have a minimum amount we know is in the solution?
        pass

        # for each letter, do we have an *exact* amount we know is in the solution?
        pass

        return hint
"""


def play_random():
    """
    pick a random solution
    at each step guess a random valid word
    return the number of guesses it takes to get the right answer
    """
    valid = range(len(wordlist))
    solution = choice(valid)
    guess_count = 0
    while True:
        guess = randint(0, len(wordlist) - 1)
        guess_count += 1

        # if we got the answer return number of guesses it took
        if guess == solution:
            return guess_count

        # otherwise filter the wordlist based on the results of this guess
        this_grade = grades[guess][solution]
        valid = [word for word in valid if grades[guess][word] == this_grade]


if __name__ == "__main__":
    histogram = Counter()
    won = 0
    tries = 10000
    for _ in range(tries):
        score = play_random()
        if score <= 6:
            won += 1

        histogram[score] += 1
    
    print(histogram)
    print(f"won {won} / {tries}")
