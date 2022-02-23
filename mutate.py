"""
a "strategy" is a set of 5 words to guess

results!

top results, round 101:
['tough', 'winks', 'pelfs', 'chyme', 'broad']: 0.9158333333333338 (alive for 34 round)
['guilt', 'skeen', 'harpy', 'combe', 'dwaal']: 0.9125000000000005 (alive for 67 round)
['guilt', 'winks', 'pelfs', 'chyme', 'broad']: 0.8966666666666673 (alive for 42 round)
['guilt', 'winks', 'roper', 'chyme', 'broad']: 0.8931111111111116 (alive for 5 round)
['mufti', 'skeen', 'harpy', 'combe', 'dwaal']: 0.8845000000000004 (alive for 9 round)

top results, round 102:
['guilt', 'winks', 'pervo', 'chyme', 'broad']: 0.9386666666666673 (alive for 8 round)
['vauts', 'winks', 'pelfs', 'chyme', 'broad']: 0.9283333333333339 (alive for 7 round)
['tough', 'winks', 'pelfs', 'chyme', 'broad']: 0.9116666666666673 (alive for 35 round)
['tarsi', 'skeen', 'harpy', 'combe', 'dwaal']: 0.9072619047619053
['guilt', 'winks', 'pelfs', 'chyme', 'broad']: 0.9033333333333338 (alive for 43 round)

top results, round 103:
['guilt', 'skeen', 'harpy', 'combe', 'dwaal']: 0.9266666666666673 (alive for 69 round)
['mufti', 'skeen', 'harpy', 'combe', 'dwaal']: 0.9141666666666672 (alive for 11 round)
['guilt', 'winks', 'pervo', 'chyme', 'broad']: 0.9064285714285719 (alive for 9 round)
['guilt', 'winks', 'pelfs', 'chyme', 'broad']: 0.9025000000000005 (alive for 44 round)
['mufti', 'skeen', 'harpy', 'combe', 'dwaal']: 0.9008333333333339 (alive for 11 round)

top results, round 104:
['guilt', 'winks', 'pelfs', 'chyme', 'broad']: 0.9333333333333339 (alive for 45 round)
['tough', 'winks', 'pelfs', 'chyme', 'broad']: 0.923333333333334 (alive for 37 round)
['mufti', 'skeen', 'harpy', 'corby', 'dwaal']: 0.9183333333333339
['vauts', 'winks', 'pelfs', 'chyme', 'broad']: 0.9141666666666673 (alive for 9 round)
['guilt', 'skeen', 'harpy', 'combe', 'dwaal']: 0.908333333333334 (alive for 70 round)

"""

import unittest
from random import sample, randint
import json


with open("wordlist.txt") as f:
    wordlist = [line.strip() for line in f]

with open("grades.json") as f:
    grades = json.load(f)

GRAY = 0
YELLOW = 1
GREEN = 2


class Strategy(object):
    def __init__(self, guesses=None):
        if guesses is None:
            self.guesses = sample(range(len(wordlist)), 5)
        else:
            self.guesses = guesses

    def __hash__(self):
        return hash(tuple(self.guesses))

    def copy(self):
        return Strategy(list(self.guesses))

    def __repr__(self):
        return str([wordlist[i] for i in self.guesses])

    def mutate(self):
        """
        create a new strategy with one word randomly mutated to a different one
        """
        new_word = randint(0, len(wordlist) - 1)
        while new_word in self.guesses:
            new_word = randint(0, len(wordlist) - 1)

        strategy = self.copy()
        strategy.guesses[randint(0, 4)] = new_word
        return strategy

    def evaluate(self, games=100):
        """
        play 'games' random games and return the average win rate
        """
        average_win_rate = 0
        for _ in range(games):
            solution = randint(0, len(wordlist) - 1)
            word_count = 0
            for word in range(len(wordlist)):
                if all(grades[guess][solution] == grades[guess][word] for guess in self.guesses):
                    word_count += 1

            average_win_rate += 1 / word_count / games

        return average_win_rate


if __name__ == "__main__":
    # start with 100 random strategies
    pool = [Strategy() for _ in range(100)]
    survival_count = dict()
    
    round = 1
    while True:
        results = sorted(((strategy, strategy.evaluate()) for strategy in pool), key=lambda pair: pair[1], reverse=True)
        print(f"top results, round {round}:")
        for strategy, score in results[:5]:
            if strategy in survival_count:
                print(f"{strategy}: {score} (alive for {survival_count[strategy]} round)")
            else:
                print(f"{strategy}: {score}")
        print()


        # keep the top 15
        best = [strategy for strategy, score in results[:15]]
        pool = list(best)
        print(len(pool))

        # for each of the top 15 add mutated versions:
        for strategy in best:
            for _ in range(5):
                pool.append(strategy.mutate())

        print(len(pool))

        # add 10 new random strategies
        for _ in range(10):
            pool.append(Strategy())

        print(len(pool))

        # update counts of how many rounds the strategies have survived
        survival_count = {strategy: survival_count.get(strategy, 0) + 1 for strategy in best}

        round += 1
