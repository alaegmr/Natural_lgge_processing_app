class StopwordsManager:
    @staticmethod
    def load_stopwords(file_path):
        """Load stopwords from a text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())

    @staticmethod
    def add_custom_stopwords(stopwords_set, custom_words):
        """Add custom stopwords to existing set"""
        stopwords_set.update(custom_words)
        return stopwords_set