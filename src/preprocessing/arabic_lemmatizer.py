from farasa.stemmer import FarasaStemmer
import logging
import time

class ArabicLemmatizer:
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.lemmatizer = self._init_lemmatizer()

    def _init_lemmatizer(self):
        for attempt in range(self.max_retries):
            try:
                lemmatizer = FarasaStemmer(interactive=False)
                if lemmatizer.stem("يدرسون"):
                    return lemmatizer
                raise ValueError("Lemmatizer returned empty result")
            except Exception as e:
                logging.warning(f"Try {attempt+1} failed: {str(e)}")
                time.sleep(self.retry_delay)
        raise RuntimeError("Failed to initialize lemmatizer")

    def _safe_lemmatize(self, word: str) -> str:
        try:
            return self.lemmatizer.stem(word)
        except Exception as e:
            logging.warning(f"Lemmatizing error for '{word}': {str(e)}")
            return word
