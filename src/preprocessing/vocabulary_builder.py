import re
from collections import defaultdict

class VocabularyBuilder:
    def __init__(self, stop_words=None):
        self.vocabulary = defaultdict(int)
        self.stop_words = stop_words or set()
        self.min_word_length = 2

    def add_text(self, text):
        """Process text and add words to vocabulary"""
        words = text.split()
        for word in words:
            if (word not in self.stop_words and
                len(word) >= self.min_word_length and
                self._is_arabic_word(word)):
                self.vocabulary[word] += 1

    def _is_arabic_word(self, word):
        """Check if word contains only Arabic letters"""
        arabic_letters = '\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF'
        return bool(re.fullmatch(f'[{arabic_letters}]+', word))

    def get_vocabulary(self):
        """Return the vocabulary dictionary"""
        return dict(self.vocabulary)