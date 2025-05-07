import os
from .file_handler import FileHandler
from .text_cleaner import TextCleaner
from .vocabulary_builder import VocabularyBuilder
from .stopwords_manager import StopwordsManager

class ArabicTextProcessor:
    def __init__(self, input_dir, output_dir, use_farasa=True):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.file_handler = FileHandler()
        self.text_cleaner = TextCleaner()

    def process_files(self, stop_words_path=None, custom_stopwords=None):
        """Main processing pipeline"""
        stopwords = self._setup_stopwords(stop_words_path, custom_stopwords)
        vocab_builder = VocabularyBuilder(stopwords)

        for file_path in self.file_handler.get_files_in_directory(self.input_dir):
            text = self.file_handler.read_text_file(file_path)
            cleaned_text = self.text_cleaner.clean_arabic_text(text)
            vocab_builder.add_text(cleaned_text)

        self._save_results(vocab_builder)

    def _setup_stopwords(self, stop_words_path, custom_stopwords):
        """Initialize and configure stopwords"""
        stopwords = set()
        if stop_words_path:
            stopwords = StopwordsManager.load_stopwords(stop_words_path)
        if custom_stopwords:
            stopwords = StopwordsManager.add_custom_stopwords(stopwords, custom_stopwords)
        return stopwords

    def _save_results(self, vocab_builder):
        """Save processing results"""
        os.makedirs(self.output_dir, exist_ok=True)
        output_path = os.path.join(self.output_dir, 'initDictionary.json')
        self.file_handler.save_vocabulary(vocab_builder.get_vocabulary(), output_path)