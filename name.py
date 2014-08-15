import random


ONSETS = [
    "b", "c", 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n',
    'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z',
    'bj', 'bl', 'br', 'ch', 'cl', 'cr', 'dr', 'fl', 'fr',
    'gh', 'gl', 'gn', 'gr', 'kh', 'kl', 'kn', 'kr', 'nh',
    'ph', 'pl', 'pr', 'sc', 'sk', 'sh', 'sl', 'st'
]


MONOTHONGS = [
    'a', 'e', 'i', 'o', 'u'
]

DIPHTHONGS = [
    'ai', 'au', 'ao',
    'ea', 'ee', 'ei', 'eo', 'ia', 'ie', 'io',
    'oa', 'oo', 'oi', 'ou', 'ua', 'ui', 'uo'
]

VOWELS = MONOTHONGS + DIPHTHONGS

CODAS = [
    'b', 'c', 'ch', 'd', 'f', 'g', 'gh', 'h', 'k', 'l', 'll', 'lk',
    'lm', 'm', 'n', 'p', 'ph', 'r', 's', 'st', 't', 'z',
]


def gen_syllable():
    onset = random.randint(0, len(ONSETS) - 1)
    vowel = random.randint(0, len(VOWELS) - 1)
    coda = random.randint(0, len(CODAS) - 1)

    syllable = ONSETS[onset] + VOWELS[vowel] + CODAS[coda]

    return syllable


def gen_word(syllable_count):
    word = ""
    for i in range(syllable_count):
        word += gen_syllable()
    return word


if __name__ == "__main__":
    print(gen_word(random.randint(1, 2)))
