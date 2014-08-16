import random
import os
import subprocess
import re
import argparse
import sys

if sys.version_info.major >= 3:
    import urllib.request as urllib2
else:
    import urllib2

# http://en.wikipedia.org/wiki/SAMPA_chart_for_English
# http://en.wikipedia.org/wiki/English_phonology

# We deliberately remove some possible sounds because we think
# they are hard to pronounce.

SINGLE_CONSONANTS = set(['p', 'b', 't', 'd', 'tS', 'dZ', 'k', 'g', 'f', 
'v', 'T', 'D', 's', 'z', 'S', 'Z', 'h',
'm', 'n', 'N', 'l', 'r', 'w', 'j', 'W', 'x', ''])

ONSETS = SINGLE_CONSONANTS - set(['N', 'x']) \
    | set(['pl', 'bl', 'kl', 'gl', 'pr', 'br', 'tr', 'dr', 'kr', 'gr', 'tw', 'dw', 'kw', 'pw']) \
    | set(['fl', 'sl', 'fr', 'hw', 'sw']) \
    | set(['sp', 'st', 'sk']) \
    | set(['sm', 'sn']) \
    | set(['sf']) \
    | set(['spl', 'spr', 'str', 'skr', 'skw'])


# Although there could be many representations for a single
# sound (e.g. ir and er for 3:). We opt for the simplest
# and least astonishing one.

ONSET_REPR = {
    'tS': 'ch',
    'dZ': 'j',
    'T': 'th',
    'D': 'th',
    'S': 'sh',
    'Z': 'z',
    'j': 'y',
    'W': 'wh',
    'kr': 'cr',
    'kw': 'qu',
    'pw': 'pu',
    'hw': 'wh',
    'sf': 'sph',
    'skr': 'scr',
    'skw': 'squ'
}


CODAS = SINGLE_CONSONANTS - set(['h', 'r', 'w', 'j', 'W', 'x']) \
    | set(['lp', 'lb', 'lt', 'ld', 'ltS', 'ldZ', 'lk']) \
    | set(['rp', 'rb', 'rt', 'rd', 'rtS', 'rdZ', 'rk', 'rg']) \
    | set(['lf', 'lv', 'lT', 'ls', 'lS']) \
    | set(['rf', 'rv', 'rT', 'rs', 'rz', 'rS']) \
    | set(['lm', 'ln']) \
    | set(['rm', 'rn', 'rl']) \
    | set(['mp', 'nt', 'nd', 'ntS', 'ndZ', 'Nk']) \
    | set(['mf', 'mT', 'nT', 'ns', 'nz', 'NT']) \
    | set(['ft', 'sp', 'st', 'sk']) \
    | set(['fT']) \
    | set(['pt', 'kt']) \
    | set(['pT', 'ps', 'ts', 'dT', 'ks']) \
    | set(['mpt', 'mps', 'ndT']) \
    | set(['kst'])


CODA_REPR = {
    'tS': 'ch',
    'dZ': 'dge',
    'k': 'ck', 
    'v': 've',
    'T': 'th',
    'D': 'th',
    's': 'ss',
    'z': 'se',
    'S': 'sh',
    'Z': 'ge',
    'N': 'ng',
    'l': 'll',
    'ltS': 'lch',
    'ldZ': 'lge',
    'rtS': 'rch',
    'rdZ': 'rge',
    'rg': 'rgue',
    'lT': 'lth',
    'ls': 'lse',
    'lS': 'lsh',
    'rv': 'rve',
    'rT': 'rth',
    'rs': 'rce',
    'rz': 'rs',
    'ntS': 'nch',
    'ndZ': 'nge',
    'Nk': 'nk',
    'mf': 'mph',
    'mT': 'mth',
    'nT': 'nth',
    'ns': 'nce',
    'nz': 'nze',
    'NT': 'ngth',
    'fT': 'fth',
    'kt': 'ct',
    'pT': 'pth',
    'ps': 'pse',
    'ts': 'tz',
    'dT': 'dth',
    'ks': 'x',
    'mps': 'mpse',
    'ndT': 'ndth',
    'kst': 'xt'
}


MONOPHTHONGS = [ 'A:', 'i:', 'I', 'E', '3:', '{', 'A:', 'V',
'Q', 'O:', 'U', 'u:', '@']


DIPHTHONGS = ['eI', 'aI', 'OI', '@U', 'aU', 'I@', 'E@', 'U@', 'ju:']


VOWELS = MONOPHTHONGS + DIPHTHONGS

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
    'aI': 'ai',
    'OI': 'oy',
    '@U': 'o',
    'aU': 'ow',
    'I@': 'ear',
    'E@': 'ere',
    'U@': 'ua',
    'ju:': 'ew'
}


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


def is_good_syllable(syl):
    """
    is_good_syllable uses some simple phonology check to rule out
    hard to pronounce syllables.
    """
    if syllable_nucleus(syl) in ["3:", '@'] \
            and syllable_coda(syl) \
            not in ['t', 'p', 'd', 'th', 'g', 'f', 'm', 'n', 'v']:
        return False

    return True



def syllable_to_repr(syl):
    """
    syllable_to_repr turns a syllable into a string representation.
    """
    nucleus = syllable_nucleus(syl)
    if nucleus in MONOPHTHONGS:
        if nucleus in MONOPHTHONG_REPR:
            nucleus_repr = MONOPHTHONG_REPR[nucleus]
    else:
        nucleus_repr = DIPHTHONG_REPR[nucleus]

    onset = syllable_onset(syl)
    onset_repr = ONSET_REPR[onset] if onset in ONSET_REPR else onset

    coda = syllable_coda(syl)
    coda_repr = CODA_REPR[coda] if coda in CODA_REPR else coda

    # FIXME: Urgently in need of refactoring
    if coda_repr == 'll' and nucleus_repr in ['ee', 'er', 'oo']:
        coda_repr = 'l'

    if coda_repr == 'ss' and nucleus_repr == 'ee':
        nucleus_repr = 'i'

    if nucleus_repr == 'i' and coda_repr == '':
        nucleus_repr = 'y'

    if nucleus_repr == 'ee' and onset_repr in ['pu', 'qu', 'squ']:
        nucleus_repr = 'i'

    if nucleus_repr == 'ee' and coda_repr == 'sp':
        nucleus_repr = 'i'

    return onset_repr + nucleus_repr + coda_repr


def gen_word(syllable_count):
    word = ""
    for i in range(syllable_count):
        syl = gen_syllable()
        while not is_good_syllable(syl):
            syl = gen_syllable()
        word += syllable_to_repr(syl)
    return word


def word_is_in_dictionary(word):
    dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'british-english')
    return subprocess.call(['grep', '^{0}$'.format(word), dict_path], stdout=subprocess.PIPE) == 0


def bing_popularity(word):
    try:
        response = urllib2.urlopen('http://www.bing.com/search?cc=us&q=' + word)
        html = response.read()

        # They found nothing and suggested something else
        if re.search(r'<div id="sp_requery"><h2>No results found for', html) != None:
            return 0

        m = re.search(r'<span class="sb_count">([0-9,.]*) results</span>', html)
        return int(m.group(1).replace(",", '').replace('.', ''))
    except:
        return 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--allow-meaningful-words",
        help="Don't use the dictionary to dismiss meaningful words.",
        action="store_true")

    parser.add_argument("--allow-popular-words",
        help="Don't use Bing to dismiss popular words.", action="store_true")

    parser.add_argument("--max-popularity",
        help="Max allowed popularity. Default is 100000.",
        type=int, default=100000, metavar="INTEGER")

    parser.add_argument("--max-syllables",
        help="Max number of syllables. Default is 1.",
        type=int, default=1, metavar="INTEGER")

    parser.add_argument("--verbose",
        help="Print more messages.", action="store_true")

    args = parser.parse_args()


    if args.allow_meaningful_words:
        def word_is_in_dictionary(word):
            return False

    if args.allow_popular_words:
        def bing_popularity(word):
            return 0

    word = ""

    def log(msg):
        if args.verbose:
            print(msg)

    while True:
        word = gen_word(random.randint(1, args.max_syllables))
        log("Trying '{0}'".format(word))

        if word_is_in_dictionary(word):
            log("Nah, it has meaning.")
        elif bing_popularity(word) > args.max_popularity:
            log("Nah, it's too popular.")
        else:
            break

    if args.verbose:
        print("'{0}' looks good.".format(word))
    else:
        print(word)

