from farasa.stemmer import FarasaStemmer
import logging
import time

class ArabicStemmer:
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.stemmer = self._init_stemmer()

    def _init_stemmer(self):
        for attempt in range(self.max_retries):
            try:
                stemmer = FarasaStemmer(interactive=False)
                test = stemmer.stem("الطلاب يدرسون في الجامعة")
                if test == "طالب درس في جامعة":
                    return stemmer
                raise ValueError("Stemming test failed")
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"Stemming init failed: {str(e)}")
                time.sleep(self.retry_delay)

    def _safe_stem(self, word: str) -> str:
        try:
            return self.stemmer.stem(word)
        except Exception as e:
            logging.warning(f"Stemming error for '{word}': {str(e)}")
            return word
