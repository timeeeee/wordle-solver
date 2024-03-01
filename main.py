import json
from sys import argv, stderr

from grades import grade
from player import WordlePlayer


with open("wordlist.txt") as f:
    wordlist = [line.strip() for line in f]


if __name__ == "__main__":
    try:
        with open("strategy.json") as f:
            strategy = json.load(f)
    except FileNotFoundError:
        print(
            ('No "strategy.json file - '
             ' generate this first using "python generate_strategy.py"'),
            file=sys.stderr)

    player = WordlePlayer(strategy)

    # if there is an argument, play wordle with it. Otherwise play all possible
    # games and show statistics
    if len(argv) == 2:
        guesses = player.play(argv[1], strategy)
        print(f"guesses: {', '.join(guesses)}")
    else:
        histogram = [0 for _ in range(10)]
        lost_words = []
        for word in wordlist:
            count = len(player.play(word, strategy))
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
