import json
from collections import defaultdict
from pathlib import Path

# ✅ Alphabet arabe standard (28 lettres)
ARABIC_ALPHABET = set("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")


def is_arabic_letter(char):
    """Vérifie si le caractère est une des 28 lettres arabes standard."""
    return char in ARABIC_ALPHABET


def load_final_vocab(file_path):
    """Charge le vocabulaire final (valide) depuis le fichier JSON."""
    with open(file_path, 'r', encoding='utf-8') as f:
        vocab_data = json.load(f)
    return {entry["word"] for entry in vocab_data if "word" in entry}


def build_char_cooccurrence_matrix_with_probabilities(corpus_path, vocab_set, output_path):
    char_matrix = defaultdict(lambda: defaultdict(int))
    total_pairs = 0
    all_chars = set()

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            for word in words:
                if word not in vocab_set:
                    continue  # Ignorer les mots hors vocabulaire

                # 🔠 Ne garder que les lettres arabes standard
                word = ''.join([char for char in word if is_arabic_letter(char)])

                for i in range(len(word) - 1):
                    c1, c2 = word[i], word[i + 1]
                    if is_arabic_letter(c1) and is_arabic_letter(c2):
                        char_matrix[c1][c2] += 1
                        total_pairs += 1
                        all_chars.update([c1, c2])

    # 🔢 Calcul des probabilités
    char_order = sorted(all_chars)
    matrix_data = []
    for from_char in char_order:
        correlations = []
        for to_char in sorted(char_matrix[from_char]):
            prob = char_matrix[from_char][to_char] / total_pairs
            prob = round(prob, 8)
            correlations.append({"to": to_char, "value": prob})
        matrix_data.append({"from": from_char, "correlations": correlations})

    result = {
        "metadata": {
            "character_order": char_order,
        },
        "matrix": {
            "data": matrix_data
        }
    }

    # 💾 Sauvegarde JSON
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[✓] Matrice de cooccurrence sauvegardée dans : {output_path}")


if __name__ == "__main__":
    # 📁 Chemins d'accès
    final_dict_path = "../../data/processed/finalDictionary.json"
    corpus_path = "../../data/processed/splittedCorpus.txt"
    output_path = "../../data/processed/char_matrix_probabilities.json"

    # 🔄 Traitement
    final_vocab = load_final_vocab(final_dict_path)
    build_char_cooccurrence_matrix_with_probabilities(corpus_path, final_vocab, output_path)
