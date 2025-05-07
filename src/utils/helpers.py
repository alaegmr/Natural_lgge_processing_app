from functools import lru_cache

def is_arabic(word):
    return any('\u0600' <= ch <= '\u06FF' for ch in word)

@lru_cache(maxsize=100_000)
def cached_stem(word, stemmer):
    return stemmer._safe_stem(word)

@lru_cache(maxsize=100_000)
def cached_lemma(word, lemmatizer):
    return lemmatizer._safe_lemmatize(word)
