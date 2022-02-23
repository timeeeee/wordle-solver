from collections import defaultdict
from string import ascii_lowercase
import unittest


with open("wordlist.txt") as f:
    wordlist = [line.strip() for line in f]


class WordleTrie(dict):
    def __init__(self, wordlist=[]):
        super().__init__()
        self.end = False
        for word in wordlist:
            self.add_word(word)
    
    def add_word(self, word):
        # if this is the last character, mark this as a word end
        if len(word) == 0:
            self.end = True
            return

        # mark this character as a valid next character from this node
        if word[0] not in self:
            self[word[0]] = WordleTrie()

        # recurse to add the rest of the word
        self[word[0]].add_word(word[1:])

    def get_valid_words(self, available_chars, required_chars):
        """
        where 'available_chars' is a list of sets indicating which characters
        are available in each spot, and 'required_chars' is a set of
        characters that must be in the finished word.

        yield all words from the trie that are possible answers to the wordle.
        """
        # base case: if no more chars to add, and all required chars used, this is a valid solution
        if len(available_chars) == 0:
            if len(required_chars) == 0:
                yield ""
        elif len(required_chars) <= len(available_chars):
            # for each character that might come next...
            for char in available_chars[0].intersection(self.keys()):
                for rest in self[char].get_valid_words(available_chars[1:], required_chars.difference([char])):
                    yield char + rest

    def is_valid_word(self, word):
        # if we're at the end of the word we've already checked all the letters
        if word == "":
            return self.end

        # if the next character isn't in this node, not in trie:
        if word[0] not in self:
            return False

        # otherwise this character is fine, check the rest
        return self[word[0]].is_valid_word(word[1:])


class WordleTrieTestCase(unittest.TestCase):
    def setUp(self):
        self.trie = WordleTrie(wordlist)

    def test_word_is_valid(self):
        for word in wordlist:
            self.assertTrue(self.trie.is_valid_word(word))

    def test_word_is_not_in_trie(self):
        self.assertFalse(self.trie.is_valid_word("boole"))
        self.assertFalse(self.trie.is_valid_word("abber"))
        self.assertFalse(self.trie.is_valid_word("abcde"))

    def test_empty_word_not_in_trie(self):
        self.assertFalse(self.trie.is_valid_word(""))

    def test_recreate_wordlist(self):
        # if there are no hints, all words are valid
        available_chars = [set(ascii_lowercase) for _ in range(5)]
        required_chars = set()
        valid_words = self.trie.get_valid_words(available_chars, required_chars)
        self.assertSetEqual(set(wordlist), set(valid_words))

    def test_find_anagram_of_cigar(self):
        available = [set(ascii_lowercase) for _ in range(5)]
        self.assertSetEqual(
            set(self.trie.get_valid_words(available, set("cigar"))),
            {"craig", "cigar"})

    def test_too_many_required_letters(self):
        available = [set(ascii_lowercase) for _ in range(4)]
        self.assertEqual(len(list(self.trie.get_valid_words(available, set("cigar")))), 0)

    def test_solve_panic(self):
        available = [set(ascii_lowercase) for _ in range(5)]
        required = set()
        self.assertIn("panic", list(self.trie.get_valid_words(available, required)))

        # guessed "pouty" - first letter in right place
        available[0] = {"p"}
        for s in available:
            for char in "outy":
                s.discard(char)
                
        self.assertIn("panic", list(self.trie.get_valid_words(available, required)))

        # guessed "rages" - second letter "a" in right place
        available[1] = {"a"}
        for s in available:
            for char in "rges":
                s.discard(char)
                
        self.assertIn("panic", list(self.trie.get_valid_words(available, required)))

        # guessed "quine" - "i" not in 3rd space, "n" not in 4th
        available[2].remove("i")
        required.add("i")
        available[3].remove("n")
        required.add("n")
        for s in available:
            for char in "que":
                s.discard(char)

        self.assertIn("panic", list(self.trie.get_valid_words(available, required)))

        # guessed "lambs": all wrong except the "a" in second position
        for s in available:
            for char in "lmbs":
                s.discard(char)
                
        self.assertIn("panic", list(self.trie.get_valid_words(available, required)))

        # guessed "panic"
        available[2] = {"n"}
        available[3] = {"i"}
        available[4] = {"c"}
        self.assertListEqual(["panic"], list(self.trie.get_valid_words(available, required)))
        


if __name__ == "__main__":
    counts = defaultdict(lambda: 0)
    trie = WordleTrie(wordlist)

    for guess in wordlist:
        for actual in wordlist:
            available = [set(ascii_lowercase) for _ in range(5)]
            required = set()
            for i in range(5):
                if actual[i] == guess[i]:
                    # correct letter in correct spot
                    available[i] = {guess[i]}
                elif guess[i] in actual:
                    # letter is in word but not here
                    available[i].remove(guess[i])
                    required.add(guess[i])
                else:
                    # the letter is not in this word
                    for s in available:
                        s.discard(guess[i])

            # now how many words are available?
            counts[guess] += len(list(trie.get_valid_words(available, required)))

        print(f"{guess}: {counts[guess]}")
            

    print(sorted(counts.items(), key=lambda pair: pair[1])[:10])
                    
                
