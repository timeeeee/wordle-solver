import unittest
from collections import Counter
import json


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


class TestGrade(unittest.TestCase):
    def test_abyss_booby(self):
        self.assertListEqual(grade("abyss", "booby"), [GRAY, YELLOW, YELLOW, GRAY, GRAY])

    def test_booby_abyss(self):
        self.assertListEqual(grade("booby", "abyss"), [YELLOW, GRAY, GRAY, GRAY, YELLOW])

    def test_sissy_essay(self):
        self.assertListEqual(grade("sissy", "essay"), [YELLOW, GRAY, GREEN, GRAY, GREEN])

    def test_essay_sissy(self):
        self.assertListEqual(grade("essay", "sissy"), [GRAY, YELLOW, GREEN, GRAY, GREEN])

        
if __name__ == "__main__":
    grades = [[hash(grade(guess, solution)) for solution in wordlist] for guess in wordlist]

    with open("grades2.json", "w") as f:
        json.dump(grades, f)
