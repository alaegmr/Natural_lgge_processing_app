from pathlib import Path
from preprocessing.main import ArabicTextProcessor
import logging
from datetime import datetime
import json

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("run1.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def load_stopwords(stopwords_path):
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        words = set()
        for word in f:
            word = word.strip()
            if word:
                normalized = (word.replace('ى', 'ي')
                              .replace('أ', 'ا')
                              .replace('إ', 'ا')
                              .replace('ة', 'ه')
                              .strip())
                words.add(normalized)
        return words

def filter_stopwords(data, stopwords):
    filtered = []
    stopwords_found = set()

    for entry in data:
        word = entry.get('word', '')
        normalized = (word.replace('ى', 'ي')
                      .replace('أ', 'ا')
                      .replace('إ', 'ا')
                      .replace('ة', 'ه')
                      .strip())
        if normalized in stopwords:
            stopwords_found.add(word)
        else:
            filtered.append(entry)

    if stopwords_found:
        logging.info(f"Stopwords filtrés : {', '.join(sorted(stopwords_found))}")
    return filtered

def main():
    start_time = datetime.now()
    base_dir = Path(__file__).parent.parent

    input_dir = base_dir / "data" / "input"
    output_dir = base_dir / "data" / "processed"
    stopwords_path = base_dir / "data" / "stopwords" / "arabic_stopwords.txt"
    dictionary_path = output_dir / "initDictionary.json"

    try:
        logging.info("Chargement des stopwords...")
        stopwords = load_stopwords(stopwords_path)
        logging.info(f"{len(stopwords)} stopwords chargés")

        logging.info("Début du prétraitement...")
        processor = ArabicTextProcessor(
            input_dir=str(input_dir),
            output_dir=str(output_dir),
            use_farasa=True
        )
        processor.process_files()

        # Lire les données générées par le prétraitement
        with open(dictionary_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Affichage du nombre total de mots AVANT traitement
        logging.info(f"\n📌 Nombre total de mots (avec stopwords) : {len(data)}")

        # Filtrage des stopwords
        original_count = len(data)
        data = filter_stopwords(data, stopwords)
        filtered_count = original_count - len(data)

        # Sauvegarde après filtrage
        with open(dictionary_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logging.info(f"Dictionnaire sauvegardé : {dictionary_path}")
        logging.info(f"Stopwords supprimés : {filtered_count} sur {original_count}")

    except Exception as e:
        logging.error(f"ERREUR: {str(e)}", exc_info=True)
    finally:
        duration = datetime.now() - start_time
        logging.info(f"Temps d'exécution : {duration.total_seconds():.2f} sec")

if __name__ == "__main__":
    main()
