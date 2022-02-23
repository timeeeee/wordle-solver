import math
from collections import defaultdict

from generate_grades import *
from play import play_wordle


with open("shortlist.txt") as f:
    wordlist = [line.strip() for line in f]

print("generating grades...")
grades = [[None for _ in wordlist] for _ in wordlist]
for guess_i, guess in enumerate(wordlist):
    for solution_i, solution in enumerate(wordlist):
        grades[guess_i][solution_i] = grade(guess, solution)


def pick_guess_expected(words_left):
    # "score" means max number of words possible in the potential next wordlists after a guess
    best_score = math.inf
    best_guess = None

    for guess in range(len(wordlist)):
        next_wordlist_counts = Counter()
        for solution in words_left:
            next_wordlist_counts[grades[guess][solution]] += 1

        # use expected list size
        expected_count = sum(count**2 for count in next_wordlist_counts.values()) / len(next_wordlist_counts)
        if expected_count < best_score:
            best_score = expected_count
            best_guess = guess

    return best_guess


def build_strategy_expected(valid_words, depth=0, debug=False):
    """
    Return a strategy for all wordle games
    
    strategy is (guess, dict of grades: rest_of_strategy)

    When there's one word left, we still have to guess it: there will be a
    strategy tuple with that word as the guess, and {all_greens: None} as the
    next moves.
    """
    if depth < 2:
        print(f"{depth*'  '}build_strategy_expected({[wordlist[i] for i in valid_words]})")

    # if there's only one word left we're done
    if len(valid_words) == 1:
        return (wordlist[valid_words[0]], {242: None})

    # otherwise, which one should we pick?
    guess = pick_guess_expected(valid_words)

    # what are the possible outcomes?
    outcomes = defaultdict(list)  # grade: list of words left with that grade
    for solution in valid_words:
        grade = grades[guess][solution]
        outcomes[grade].append(solution)

    # now decide what to do in case of each possible grade for our guess
    next_moves = dict()
    for grade, next_valid_words in outcomes.items():
        next_moves[grade] = build_strategy_expected(next_valid_words, depth+1)

    return (wordlist[guess], next_moves)


if __name__ == "__main__":
    print("building tree...")
    tree = build_strategy_expected(range(len(wordlist)))
    
    histogram = [0 for _ in range(10)]
    for solution in wordlist:
        histogram[len(play_wordle(solution, tree))] += 1

    average = sum(i * x for i, x in enumerate(histogram)) / sum(histogram)

    print(histogram)
    print(f"average: {average}")
    
