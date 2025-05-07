import json
import time
import logging
import chardet
from pathlib import Path
from preprocessing.arabic_stemmer import ArabicStemmer
from preprocessing.arabic_lemmatizer import ArabicLemmatizer
from preprocessing.arabic_ner import ArabicNER
from utils.helpers import is_arabic, cached_stem, cached_lemma

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_arabic_dictionary(dict_path):
    arabic_words = set()
    for file_path in dict_path.glob("*.txt"):
        with open(file_path, 'rb') as raw_file:
            encoding = chardet.detect(raw_file.read())['encoding'] or 'utf-8'
        with open(file_path, 'r', encoding=encoding) as f:
            for line in f:
                word = line.strip().split("/")[0]
                if word:
                    arabic_words.add(word)
    return arabic_words

def process_word(entry, arabic_words, stemmer, lemmatizer, ner_holder):
    word = entry["word"]
    word_id = entry["id"]

    if not is_arabic(word):
        return None, "rejected"

    if word in arabic_words:
        return {"id": word_id, "word": word}, "dictionary"
    if (stem := cached_stem(word, stemmer)) in arabic_words:
        return {"id": word_id, "word": word}, "stem"
    if (lemma := cached_lemma(word, lemmatizer)) in arabic_words:
        return {"id": word_id, "word": word}, "lemma"
    if ner_holder["ner"] is None:
        ner_holder["ner"] = ArabicNER()
    if ner_holder["ner"]._safe_recognize(word):
        return {"id": word_id, "word": word}, "ner"

    return None, "rejected"

def main():
    base_dir = Path(__file__).parent.parent  # Remonter de 2 niveaux à partir de 'src' pour atteindre la racine
    input_path = base_dir / "data" / "processed" / "initDictionary.json"
    final_path = base_dir / "data" / "processed" / "finalDictionary.json"
    rejected_path = base_dir / "data" / "processed" / "RejectedVocab.json"
    arabic_dict_dir = base_dir / "data" / "ArabicDictionary"

    arabic_words = load_arabic_dictionary(arabic_dict_dir)
    with open(input_path, 'r', encoding='utf-8') as f:
        init_data = json.load(f)

    stemmer = ArabicStemmer()
    lemmatizer = ArabicLemmatizer()
    ner_holder = {"ner": None}

    final_dict, rejected = [], []
    stats = {k: 0 for k in ["dictionary", "stem", "lemma", "ner", "rejected"]}

    for entry in init_data:
        result, method = process_word(entry, arabic_words, stemmer, lemmatizer, ner_holder)
        if result:
            final_dict.append(result)
        else:
            rejected.append({"id": entry["id"], "word": entry["word"]})
        stats[method] += 1

    with open(final_path, 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
    with open(rejected_path, 'w', encoding='utf-8') as f:
        json.dump(rejected, f, ensure_ascii=False, indent=2)

    total = sum(stats.values())
    for method, count in stats.items():
        logging.info(f"{method}: {count} ({(count / total) * 100:.2f}%)")

if __name__ == "__main__":
    main()
