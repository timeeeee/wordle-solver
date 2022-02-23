from collections import Counter

import nltk


if __name__ == "__main__":
    with open("wordlist.txt") as f:
        wordlist = [line.strip() for line in f]

    word_set = set(wordlist)
    corpus = nltk.corpus.brown
    counts = Counter()
    for word in corpus.words():
        if len(word) == 5 and word in word_set:
            counts.update([word])

    print(", ".join(word for word in wordlist if word not in counts))
