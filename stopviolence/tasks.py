from . import normalize
from .models import add_ngram


def process_language(bd):
    for bigrams in (normalize.ngrams(b.text) for b in bd.blogentry_set.all()):
        for bigram in bigrams:
            add_ngram(bigram, bd.pk)
