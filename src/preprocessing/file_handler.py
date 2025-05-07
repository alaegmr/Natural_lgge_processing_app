import os
import json
from farasa.segmenter import FarasaSegmenter


class FileHandler:
    @staticmethod
    def read_text_file(file_path):
        """Read a text file with UTF-8 encoding"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def get_files_in_directory(directory, extension='.txt'):
        """Get all files with given extension in directory"""
        return [os.path.join(directory, f) for f in os.listdir(directory)
                if f.endswith(extension)]

    @staticmethod
    def save_vocabulary(vocabulary, output_path):
        """Save vocabulary to JSON file"""
        vocab_list = [{"id": idx, "word": word, "frequency": freq}
                      for idx, (word, freq) in enumerate(vocabulary.items(), 1)]

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(vocab_list, f, ensure_ascii=False, indent=4)


    class FileHandler:
        def __init__(self):
            self.segmenter = FarasaSegmenter(interactive=False)

        def process_with_farasa(self, text):
            return self.segmenter.segment(text)