import sys
import re
import string

infile = sys.argv[1] if len(sys.argv)>=2 else './input/1.in'

text, clues = open(infile).read().strip().split("\n\n")
sentences = re.split(r'[.?!]+', text)  # separate text into sentences

sentences = sentences[:-1]  # strip off empty entry

# Load dictionary - make lower case
word_list = []
for w in open("american-english").read().strip().split("\n"):
    word_list.append(w.lower())



def apply_map(puzzle, blank, mapping):
    """"""

    for key, val in mapping.items():
        for i, sentence in enumerate(puzzle):
            for ii, word in enumerate(sentence):
                for iii, letter in enumerate(word):
                    if letter in mapping.keys():
                        blank[i][ii][iii] = mapping[letter]

    return blank


unique_chars = set()

# Construct puzzle and solution structures
puzzle, solution = [], []

for s in sentences:
    q, b = [], []
    words = s.split()
    for w in words:
        qq, bb = [], [] 
        chars = list(w)
        for c in chars:
            unique_chars.add(c.lower())
            qq.append(c.lower())
            bb.append("")

        q.append(qq)
        b.append(bb)

    puzzle.append(q)
    solution.append(b)

print(f"\nPuzzle:\n{puzzle}")


letter_map = {}
for u in unique_chars:
    letter_map[u] = ""

clues = str(clues.split(":  ")[1]).split(',')[:-1]

for c in clues:
    key, val = c.split(":")
    letter_map[key.lower()] = val.lower()

print(f"\nClues given:  {clues}")

print(f"\nUnique characters in puzzle:\n{unique_chars}")
print(f"\nCurrent letter map:  {letter_map}")

filled = apply_map(puzzle, solution, letter_map)
print(f"\nMap applied to blank puzzle:\n{filled}")



def is_full(puzzle):
    """Checks is all blanks are populated"""

    full = True
    for sentence in puzzle:
        for word in sentence:
            if "" in word:
                return False

    return True

def all_words(puzzle, word_list):
    """Checks if all fully populated 'words' are in dictionary"""

    for sentence in puzzle:
        for word in sentence:
            if "".join(word) not in word_list:
                return False

    return True


while not (all_words(solution, word_list) and is_full(solution)):

    # Based on current mapping, find available letters
    used_letters = []
    for l in list(letter_map.values()):
        if l != "":
            used_letters.append(l)

    print(f"\nUsed letters:  {used_letters}")

    remaining_letters = []
    for l in list(string.ascii_lowercase):
        if l not in used_letters:
            remaining_letters.append(l)

    print(f"\nRemaining letters: {remaining_letters}")


    # Find next letter map to try:
    for key, val in letter_map.items():
        if val == '':
            letter_map[key] = remaining_letters[0]
            break
    print(f"\nUpdated map:  {letter_map}")

    solution = apply_map(puzzle, solution, letter_map)

    print(f"\nNew map applied:  {solution}")


print(solution)
