import re
from pathlib import Path
import logging
import sys


class ArabicTextSplitter:
    def __init__(self):
        self.delimiters = r'(؟+|\!+|\.+|\۔+|\。+|\,+)'

    def clean_sentence(self, sentence):
        sentence = re.sub(r'\s+', ' ', sentence).strip()
        if not re.search(r'[.؟!۔,،]$', sentence):
            sentence += '.'
        return sentence

    def split_text(self, text):
        phrases = re.split(r'(?<=[.؟!۔,،])\s+', text)
        clean_phrases = [self.clean_sentence(p) for p in phrases if len(p.split()) >= 2]
        return clean_phrases


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    # Chemins
    project_root = Path(__file__).parent.parent.parent
    input_dir = project_root / "data" / "input"
    output_dir = project_root / "data" / "processed"
    output_file = output_dir / "splittedCorpus.txt"
    output_dir.mkdir(parents=True, exist_ok=True)

    splitter = ArabicTextSplitter()

    txt_files = list(input_dir.glob("*.txt"))
    if not txt_files:
        logging.error(f"Aucun fichier .txt trouvé dans : {input_dir}")
        sys.exit(1)

    all_sentences = []

    for file_path in txt_files:
        try:
            logging.info(f"Traitement du fichier : {file_path.name}")
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            sentences = splitter.split_text(text)
            all_sentences.extend(sentences)
            logging.info(f"{len(sentences)} phrases extraites de {file_path.name}")

        except Exception as e:
            logging.error(f"Erreur pendant le traitement de {file_path.name} : {str(e)}")

    # Sauvegarde unique de toutes les phrases dans un seul fichier
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write("\n".join(all_sentences))

    logging.info(f"\n✅ Total de {len(all_sentences)} phrases écrites dans {output_file.name}")

if __name__ == "__main__":
    main()
