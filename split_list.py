"""
Each guess has a distribution of ...

99.5% win rate! (for max strategy 12901 / 12972, for average 12908 / 12972)

takes 45s to calculate second guesses

with first and second guesses, takes ~18 minutes to play all games!
"""

import unittest
from random import sample, randint
import json
from collections import Counter, defaultdict
import math
from sys import argv


with open("wordlist.txt") as f:
    wordlist = [line.strip() for line in f]

with open("grades.json") as f:
    grades = json.load(f)

GRAY = 0
YELLOW = 1
GREEN = 2


def pick_guess_max(words_left, blacklist=set([])):
    # "score" means max number of words possible in the potential next wordlists after a guess
    max_best_score = math.inf
    max_best_guess = None

    for guess in range(len(wordlist)):
        next_wordlist_counts = Counter()
        for solution in words_left:
            next_wordlist_counts[grades[guess][solution]] += 1

        # use max
        worst_count = max(next_wordlist_counts.values())
        if worst_count < max_best_score and guess not in blacklist:
            max_best_score = worst_count
            max_best_guess = guess

    return max_best_guess


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


def pick_guess(words_left, blacklist=set([])):
    return pick_guess_max(words_left, blacklist=blacklist)


def build_strategy_max(valid_words, depth=0, debug=False):
    """
    Return a strategy for all wordle games
    
    strategy is (guess, dict of grades: rest_of_strategy)

    When there's one word left, we still have to guess it: there will be a
    strategy tuple with that word as the guess, and {all_greens: None} as the
    next moves.
    """
    if depth < 2:
        print(f"{depth*'  '}build_strategy_max({[wordlist[i] for i in valid_words]})")

    # if there's only one word left we're done
    if len(valid_words) == 1:
        return (wordlist[valid_words[0]], {242: None})

    # otherwise, which one should we pick?
    guess = pick_guess_max(valid_words)

    # what are the possible outcomes?
    outcomes = defaultdict(list)  # grade: list of words left with that grade
    for solution in valid_words:
        grade = grades[guess][solution]
        outcomes[grade].append(solution)

    # now decide what to do in case of each possible grade for our guess
    next_moves = dict()
    for grade, next_valid_words in outcomes.items():
        next_moves[grade] = build_strategy_max(next_valid_words, depth+1)

    return (wordlist[guess], next_moves)


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


def play_wordle(solution_word):
    print(f'playing wordle with solution "{solution_word}"')
    solution = wordlist.index(solution_word)
    valid_words = range(len(wordlist))

    guess_count = 0
    guesses = []
    while len(valid_words) > 1:
        if guess_count == 0:
            # first guess is "serai" with index 10424
            # nope, "nears"
            guess = wordlist.index("nears")
        # elif guess_count == 1:
            # guess = second_guesses[this_grade]
        else:
            guess = pick_guess(valid_words)

        guesses.append(guess)

        print(f"guessing {wordlist[guess]}... ", end="")
        this_grade = grades[guess][solution]
        valid_words = [i for i in valid_words if grades[guess][i] == this_grade]
        print(f"{len(valid_words)} left")
        guess_count += 1

    print(f"last possible word is {wordlist[valid_words[0]]}")
    print(f"solved wordle in {guess_count + 1} guesses")
    print(flush=True)

    if guesses[-1] != solution:
        guesses.append(valid_words[0])

    return len(guesses) < 6


if __name__ == "__main__":
    print("generating table...")
    strategy = build_strategy_expected(range(len(wordlist)))

    with open("strategy_expected.json", "w") as f:
        json.dump(strategy, f)

    exit(0)


    print("using max: ", end="")
    first = pick_guess_max(range(len(wordlist)))
    print(wordlist[first])
    print("generating strategy...")
    with open("max_strategy.json", "w") as f:
        json.dump(build_strategy_max(), f)

    print()

    print("using expected: ", end="")
    first = pick_guess_expected(range(len(wordlist)))
    print(wordlist[first])
    print("generating strategy...")
    with open("expected_strategy.json", "w") as f:
        json.dump(build_strategy_expected(), f)

    exit(0)

    games = {}
    for word in wordlist:
        games[word] = play_wordle(word)

    print("using max:")
    print(sum(1 if len(k) <= 6 else 0 for k in games.values()))
    
    
    '''
    scores = {}
    for guess, guess_word in enumerate(wordlist):
        if guess % 100 == 0:
            print(f"{guess} / {len(wordlist)}")

        grade_counts = Counter()
        for solution in range(len(wordlist)):
            grade_counts[grades[guess][solution]] += 1

        """
        I used to do this:

        average_next_wordlist_size = 0
        for grade, grade_count in grade_counts.items():
            next_wordlist_size = 0
            for word in range(len(wordlist)):
                if grade == grades[guess][word]:
                    next_wordlist_size += 1
            average_next_wordlist_size += grade_count / next_wordlist_size

        ... but next_wordlist_size always equals grade_count
        ... plus I needed to normalize by total number of grade counts too
        """
        # either use the average inverse size of these lists
        ...  # how?

        # or use the maximum next_wordlist size as a measure (smaller is better!)
        scores[guess] = 1 / max(grade_counts.values())

    with open("split_list_results.json", "w") as f:
        json.dump(scores, f, indent=4)

    for guess, score in sorted(scores.items(), key=lambda pair: pair[1], reverse=True)[:100]:
        print(f"{wordlist[guess]}: {score}")
        
    '''
