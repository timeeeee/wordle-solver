import json
from collections import defaultdict
import unittest


with open("wordlist.txt") as f:
    wordlist = [line.strip() for line in f]


print("loading grades...", end="", flush=True)
with open("grades.json") as f:
    grades = json.load(f)
print(" done.", flush=True)


GRAY = 0
YELLOW = 1
GREEN = 2


def sample(valid_words, guesses_left, samples=100):
    """
    Pick a random word from valid_words to be the solution.

    At each step, guess a random word 
    """


def expected_win_rate(valid_words, guesses_left, sample_depth=3, samples=100):
    # if there is one valid solution we will definitely get it
    if len(valid_words) == 1:
        return 1
    
    # if we're down to one guess it's up to chance
    if guesses_left == 1:
        return 1 / len(valid_words)

    # otherwise, evaluate all our options:
    # for each possible guess...
    best_win_rate = -1
    best_guess = None
    for guess in range(len(wordlist)):
        if guesses_left >= 3:
            indent = "  " * (6 - guesses_left)
            print(f"{indent}trying word {wordlist[guess]}...", flush=True)

        # what are the grades we could get from each possible solution?
        solutions_by_grade = defaultdict(list)
        for solution in valid_words:
            solutions_by_grade[grades[guess][solution]].append(solution)

        # based on these possible outcomes what's the expected win rate?
        win_rate = 0
        for grade, sub_wordlist in solutions_by_grade.items():
            win_rate += expected_win_rate(sub_wordlist, guesses_left - 1) * len(sub_wordlist)

        win_rate /= len(valid_words)

        # check if this is the best guess so far:
        if win_rate > best_win_rate:
            best_win_rate = win_rate
            best_guess = guess

    # indent = " " * 2 * (6 - guesses_left)
    # print(f"{indent}guessed {wordlist[best_guess]}")

    # save this guess in this position?
    pass

    # assuming we are going to only make good choices...
    return best_win_rate


class TestExpectedWinRate(unittest.TestCase):
    def test_one_word_left(self):
        self.assertEqual(expected_win_rate([100], 6), 1)

    def test_one_word_last_guess(self):
        self.assertEqual(expected_win_rate([100], 1), 1)

    def test_two_words_two_guesses(self):
        self.assertEqual(expected_win_rate([100, 1000], 2), 1)

    def test_two_words_last_guess(self):
        self.assertEqual(expected_win_rate([100, 1000], 1), 1 / 2)

    def test_ten_words_last_guess(self):
        self.assertEqual(expected_win_rate(list(range(10)), 1), 1/10)

    def test_almost_finished_wince_one_guess(self):
        """
        ['wince', 'bicep', 'cided', 'civie', 'diced', 'viced'] left
        """
        self.assertEqual(expected_win_rate([217, 1827, 3931, 3957, 4581, 12246], 1), 1/6)

    def test_almost_finished_wince_two_guesses(self):
        """
        ['wince', 'bicep', 'cided', 'civie', 'diced', 'viced'] left
        with two guesses, should be able to get the right word
        """
        self.assertEqual(expected_win_rate([217, 1827, 3931, 3957, 4581, 12246], 2), 1)


if __name__ == "__main__":
    overall_win_rate = expected_win_rate(list(range(len(wordlist))), 6)
    print(f"overall win rate: {overall_win_rate}")
