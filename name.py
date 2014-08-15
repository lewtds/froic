import random
import os
import subprocess
import urllib2
import re


# http://en.wikipedia.org/wiki/SAMPA_chart_for_English

CONSONANTS = set(['p', 'b', 't', 'd', 'tS', 'dZ', 'k', 'g', 'f', 
'v', 'T', 'D', 's', 'z', 'S', 'Z', 'h',
'm', 'n', 'N', 'l', 'r', 'w', 'j', 'W', 'x', ''])

ONSETS = CONSONANTS - set(['N', 'x'])
CODAS = CONSONANTS - set(['h', 'r', 'w', 'j', 'W', 'x'])


MONOPHTHONGS = [ 'A:', 'i:', 'I', 'E', '3:', '{', 'A:', 'V',
'Q', 'O:', 'U', 'u:', '@']


DIPHTHONGS = ['eI', 'aI', 'OI', '@U', 'aU', 'I@', 'E@', 'U@', 'ju:']


VOWELS = MONOPHTHONGS + DIPHTHONGS


def syllable_nucleus(syl):
    return syl[1]


def syllable_onset(syl):
    return syl[0]


def syllable_coda(syl):
    return syl[2]


def gen_syllable():
    onset = random.randint(0, len(ONSETS) - 1)
    coda = random.randint(0, len(CODAS) - 1)

    if random.randint(0, 1) == 0:
        nucleus = random.randint(0, len(MONOPHTHONGS) - 1)
        syllable = (list(ONSETS)[onset], MONOPHTHONGS[nucleus], list(CODAS)[coda])
    else:
        nucleus = random.randint(0, len(DIPHTHONGS) - 1)
        syllable = (list(ONSETS)[onset], DIPHTHONGS[nucleus], '')

    return syllable


def syllable_to_repr(syl):
    """
    syllable_to_repr turns a syllable into a string representation.
    """
    # Although there could be many representations for a single
    # monophthong (e.g. ir and er for 3:). We opt for the simplest
    # and least astonishing one.
    MONOPHTHONG_REPR = {
        'A:': 'a',
        'i:': 'ee',
        'I': 'i',
        'E': 'e',
        '3:': 'er',
        '{': 'a',
        'V': 'u',
        'Q': 'o',
        'O:': 'o',
        'U': 'u',
        'u:': 'oo',
        '@': 'er'
    }

    DIPHTHONG_REPR = {
        'eI': 'ay',
        'aI': 'y',
        'OI': 'oy',
        '@U': 'o',
        'aU': 'ow',
        'I@': 'ear',
        'E@': 'ere',
        'U@': 'air',
        'ju:': 'u'
    }

    nucleus = syllable_nucleus(syl)
    nucleus_repr = MONOPHTHONG_REPR[nucleus] \
        if nucleus in MONOPHTHONGS else DIPHTHONG_REPR[nucleus]

    ONSET_REPR = {
        'tS': 'ch',
        'dZ': 'j',
        'T': 'th',
        'D': 'th',
        'S': 'sh',
        'Z': 'z',
        'j': 'y',
        'W': 'wh',
        '': ''
    }

    onset = syllable_onset(syl)
    onset_repr = ONSET_REPR[onset] if onset in ONSET_REPR else onset

    CODA_REPR = {
        'tS': 'ch',
        'dZ': 'dge',
        'k': 'ck', 
        'v': 've',
        'T': 'th',
        'D': 'the',
        's': 'ss',
        'z': 'se',
        'S': 'sh',
        'Z': 'ge',
        'N': 'ng',
        'l': 'll'
    }

    coda = syllable_coda(syl)
    coda_repr = CODA_REPR[coda] if coda in CODA_REPR else coda

    if coda_repr == 'll' and nucleus_repr == 'ee':
        coda_repr = 'l'

    return onset_repr + nucleus_repr + coda_repr


def gen_word(syllable_count):
    word = ""
    for i in range(syllable_count):
        word += syllable_to_repr(gen_syllable())
    return word


def word_is_in_dictionary(word):
    dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'british-english')
    return subprocess.call(['grep', '^{0}$'.format(word), dict_path], stdout=subprocess.PIPE) == 0


def bing_popularity(word):
    try:
        response = urllib2.urlopen('http://www.bing.com/search?cc=us&q=' + word)
        html = response.read()

        # They found nothing and suggested something else
        if re.search(r'<div id="sp_requery">', html) != None:
            return 0

        m = re.search(r'<span class="sb_count">([0-9,.]*) results</span>', html)
        return int(m.group(1).replace(",", '').replace('.', ''))
    except Exception, e:
        return 0


if __name__ == "__main__":
    word = gen_word(random.randint(1, 2))
    while word_is_in_dictionary(word) or bing_popularity(word) > 100000:
        word = gen_word(random.randint(1, 2))

    print(word)

