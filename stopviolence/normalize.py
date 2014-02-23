import re

from django.forms.fields import validators
from django.utils.html import strip_tags

import bs4
import pymorphy2
from nltk import bigrams
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
    text = validators.URLValidator.regex.sub('', text)

    try:
        text = bs4.BeautifulSoup(text).text
    except UnicodeEncodeError:
        text = strip_tags(text)

    gen = tokenizer.tokenize(text)
    return (morph_e.stem(t) if is_english.match(t) else maybe_first_form(morph.parse(t)) or t
            for t in gen)


def ngrams(text):
    return bigrams(normalize(text))
