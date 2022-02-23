To play with a particular solution:

    python3 play.py <word>


To run for every possible solution in wordlist.txt:

    python3 play.py


# How this works:

At the beginning of a game of Wordle, the list of possible solutions is the entire wordlist from wordlist.txt (grabbed from the javascript source of Wordle pre-NYT purchase). After each guess, the resulting grade allows us to cross a number of words off of this list for the next round.

For a particular guess, there are a number of possible grades based on the 


# Tricks

I found that while grading is fast for one word, doing it len(wordlist) * len(wordlist) times is very slow. I pre-computed 

    python3 generate_grades.py


# Some other strategies:

## Guess random words from the remaining possibilities

    python3 random_valid_guess.py <word>
    python3 random_valid_guess.py

Start with the wordlist as a list of possible solutions. Until we've found the solution:

- pick a guess from the remaining possible solutions
- if it's not correct, remove words from the list that don't match the grade

Since this solution involves randomness, running this script without arguments will try each possible solution 5 times and show statistics on the results.


## Pick 5 words that give you the highest probability of getting the sixth guess correctly

    python3 evolve_five_guesses.py

This script will run until killed.




For games with a random solution, where each guess is a random word from the
list of remaining valid words, the computer wins ~5/6 of the time.


For each possible guess, what is the expected number of turns it will take to
find the solution?

for each possible solution:
  run each possible game??
