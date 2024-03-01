To play with a particular solution:

    python3 play.py <word>

To run for every possible solution in wordlist.txt and show statistics:

    python3 play.py


# How this works:

At the beginning of a game of Wordle, the list of possible solutions is the entire wordlist from wordlist.txt (grabbed from the javascript source of Wordle pre-NYT purchase). After each guess, the resulting grade allows us to cross a number of words off of this list for the next round. The more words we can rule out, the better the guess was.

At each stage we should pick the guess that, on average across all solutions that are still possible, leaves us with the smallest wordlist for the next round. I'm assuming that each possible solution is equally probable.

All this takes a while to calculate, so I generated a "strategy tree" representing guesses for all possible games. Each node has a guess, and a child for every possible grade for that guess pointing to a sub-strategy for the rest of the game. It takes <4 minutes to generate the strategy tree on my computer, and the resulting json file is about .5 MB.

# How good is it?

This strategy can solve 99.68% of the possible Wordles in 6 guesses or less. The average number of guesses is ~4.25.

# Grading

In grades.py I designated GRAY = 0, YELLOW = 1, and GREEN = 2. I created a Grade class, primarily so that I could define a hash function for it and use it as a key in dictionaries.

The actual grading was a little trickier than I thought! For example, if the solution is "abyss" and I guess "sissy":

- The last 's' in my guess is green, because it's the right letter in the right place
- The first 's' in my guess is yellow, because it's the right letter in the wrong place
- The second 's' in my guess is gray! The first 's' corresponds to the last 's' in abyss and there are no 's's left for this tile.

I found that while grading is fast for one word, doing it len(wordlist) * len(wordlist) times is very slow. Pre-computing grades speeds things up considerably. Running

    python3 grades.py

... will create a 2d list "grades" where grade[guess_index][solution_index] is the hash of the resulting grade, and dump it to "grades.json". This format is a little convoluted but makes "grades.json" more compact (~600 MB). It takes about 16 minutes to generate on my computer, and about 10 seconds to load from the finished json file into memory in a python script.

# Some other strategies:

## Guess random words from the remaining possibilities

    python3 random_valid_guess.py <word>
    python3 random_valid_guess.py

Start with the wordlist as a list of possible solutions. Until we've found the solution:

- pick a guess from the remaining possible solutions
- if it's not correct, remove words from the list that don't match the grade

Since this solution involves randomness, running this script without arguments will try each possible solution 5 times and show statistics on the results.

This strategy seems to have about 5/6 success rate.

## Pick 5 words that give you the highest probability of getting the sixth guess correctly

    python3 evolve_five_guesses.py

This script will run until killed. In each round it will keep the most successful word groups from the last round, introduce some one-word variations on them, and add some entirely new randomly generated strategies. I don't know very much about genetic algorithms and did not even try recombination, but was able to generate some strategies that had a 90% success rate.
