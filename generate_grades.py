import json

from grades import grade


with open("wordlist.txt") as f:
    wordlist = [line.strip() for line in f]

grades = [[hash(grade(guess, solution)) for solution in wordlist] for guess in wordlist]

with open("grades.json", "w") as f:
    json.dump(grades, f)
