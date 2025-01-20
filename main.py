import sys
import re
import string
import copy
infile = sys.argv[1] if len(sys.argv)>=2 else './input/1.in'

text, clues = open(infile).read().strip().split("\n\n")

sentences = re.split(r'[.?!]+', text)  # separate text into sentences
sentences = sentences[:-1]  # strip off empty entry
# Create nested list representation of the cryptogram
crypto, unique_chars = [], set()
for s in sentences:
    temp = []
    for word in s.split():
        temp2 = []
        for char in list(word):
            temp2.append(char.lower())
            unique_chars.add(char.lower())
        temp.append(temp2)
    crypto.append(temp)

print(f"\nCryptogram:  {crypto}")
print(f"\nUnique characters:  {unique_chars}")


clues = clues.split(":  ")[1]
clues = clues.split(",")[:-1]

clue_dict = {}
for c in clues:
    key, val = c.split(":")
    clue_dict[key.lower()] = val.lower()

print(f"\nDictionary of clues:  {clue_dict}")


# Construct letter map dictionary
char_map = {}
for u in unique_chars:
    char_map[u] = ""


remaining_letters = list(string.ascii_lowercase)

# Insert clue into map
for key, val in clue_dict.items():
    remaining_letters.remove(key)
    char_map[key] = val

print(f"\nCharacter map: {char_map}")
print(f"\nRemaining characters: {remaining_letters}")

# Load list of words
dictionary = []
for w in open("word-list-2").read().strip().split("\n"):
    dictionary.append(w.lower())

#print(word_list)
#print('trot' in word_list)
#input()

seen_words = set()

def next_key(char_map):
    """Determine next empty spot in character map"""

    for key, val in char_map.items():
        if val == "":
            return key

    return -1


def is_valid(char_map, k, v):
    """"""

    new_map = copy.deepcopy(char_map)
    new_map[k] = v

    for sentence in crypto:
        for word in sentence:
            word_list, filled = [], True

            for letter in word:
                new_char = new_map[letter]

                if new_char == "":
                    filled = False
                
                word_list.append(new_map[letter])

            if filled:
                w = ''.join(word_list) 
                if w in seen_words:
                    #print(f"Word found:  {w}")
                    pass
                elif w in dictionary:
                    seen_words.add(w)
                    pass
                else:
                    #print(f"Word not in dictionary:  {w}")
                    return False

    return True



def solve(char_map):

    ct = 0
    for k, v in char_map.items():
        if v != "":
            ct += 1

    print(f"{ct} populated entries in the map")
    print(char_map)

    nextKey = next_key(char_map)

    if nextKey == -1:
        solution = char_map
        print(solution)
        return True

    for l in string.ascii_lowercase:
        if l not in char_map.values():

            if is_valid(char_map, nextKey, l):
                char_map[nextKey] = l

                if solve(char_map) == False:
                    char_map[nextKey] = ""
                else:
                    return True

    return False


solve(char_map)


