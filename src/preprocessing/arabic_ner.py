from farasa.ner import FarasaNamedEntityRecognizer
import logging
import time

class ArabicNER:
    def __init__(self, max_retries=3, retry_delay=1.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.ner = self._initialize_ner()

    def _initialize_ner(self):
        for attempt in range(self.max_retries):
            try:
                ner = FarasaNamedEntityRecognizer(interactive=False)
                result = ner.recognize("محمد من القاهرة")
                if result:
                    return ner
                raise ValueError("NER test failed")
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"NER init failed: {str(e)}")
                time.sleep(self.retry_delay)

    def _safe_recognize(self, text):
        try:
            context = f"جملة تحتوي على: {text}. وهذا مثال للتحليل."
            raw_output = self.ner.recognize(context)
            return "B-" in raw_output or "I-" in raw_output
        except Exception as e:
            logging.error(f"NER error for '{text[:15]}': {str(e)}")
            return False
