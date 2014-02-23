import re

import bs4
import pymorphy2
from nltk.stem import SnowballStemmer
from nltk.tokenize import PunktWordTokenizer

morph = pymorphy2.MorphAnalyzer()
tokenizer = PunktWordTokenizer()
morph_e = SnowballStemmer('english')
is_english = re.compile('[a-zA-Z]+')


def maybe_first_form(list_):
    try:
        return list_[0].normal_form
    except IndexError:
        return None


def normalize(text):
    gen = tokenizer.tokenize(bs4.BeautifulSoup(text).text)
    return (morph_e.stem(t) if is_english.match(t) else maybe_first_form(morph.parse(t)) or t
            for t in gen)
