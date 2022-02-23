"""
top words for first pick:
serai 697
reais 769
soare 769
paseo 776
aeros 801
kaies 821
nares 823
nears 823
reans 823
stoae 825
... so first one I know is nears
"""

import unittest
from random import sample, randint
import json
from collections import Counter, defaultdict
import math
import pickle


with open("blacklist.txt") as f:
    blacklist = set(line.strip() for line in f)

with open("wordlist.txt") as f:
    wordlist = [line.strip() for line in f]

with open("whitelist.txt") as f:
    whitelist = [line.strip() for line in f]

with open("grades.json") as f:
    grades = json.load(f)

GRAY = 0
YELLOW = 1
GREEN = 2



def pick_guess(words_left):
    # "score" means max number of words possible in the potential next wordlists after a guess
    best_score = math.inf
    best_guess = None

    for guess in range(len(wordlist)):
        next_wordlist_counts = Counter()
        for solution in words_left:
            next_wordlist_counts[grades[guess][solution]] += 1

        # use max
        worst_count = max(next_wordlist_counts.values())
        if worst_count < best_score:
            best_score = worst_count
            best_guess = guess

    return best_guess


def test_pick_guess():
    assert wordlist[pick_guess(range(len(wordlist)))] == "nears"


def build_tree(valid_words, depth=0):
    """
    pick a guess...
    then build future guesses by each possible result from this guess

    return a tuple: guess, then dict of (grade, subtree) pairs
    """
    # LOGGING:
    if depth == 1:
        print("trying a second guess")

    # base case: one guess left, just return the list of options left
    if depth == 5:
        return [wordlist[word] for word in valid_words]

    # base case: one possible word left! return a list with just this one word
    if len(valid_words) == 1:
        return [wordlist[word] for word in valid_words]

    # guess "nears" the first time, calculate a guess after that
    if depth == 0:
        guess = wordlist.index("nears")
    else:
        guess = pick_guess(valid_words)

    # get the wordlists for each grade
    wordlist_by_grade = defaultdict(list)
    for solution in valid_words:
        wordlist_by_grade[grades[guess][solution]].append(solution)

    rest_of_game = dict()
    for grade, next_wordlist in wordlist_by_grade.items():
        rest_of_game[grade] = build_tree(next_wordlist, depth + 1)

    return (guess, rest_of_game)


class TestBuildTree(unittest.TestCase):
    def test_one_word_left(self):
        self.assertListEqual(build_tree(["moist"]), ["moist"])


if __name__ == "__main__":
    # build a tree for the whole game!
    valid_words = [index for index, word in enumerate(wordlist) if word not in blacklist]
    tree = build_tree(valid_words)
    with open("tree.pkl", "wb") as f:
        pickle.dump(tree, f)
